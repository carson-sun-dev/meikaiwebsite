"""
Jieba 中文分词器(单例)+ 装修自定义词典。

DESIGN §5.6.1 决策(关键):
- 不用 Qdrant 服务端 ICU 分词:对"踢脚线/吊顶/水电铺设"等装修专业术语零领域知识,
  会被切碎成单字,BM25 召回率极差
- 改走 Jieba 客户端预 tokenize:加载从 23 份历史预算单 ETL 抽取的 ~300 词装修词典,
  保证术语整词命中
- 强制纪律:`tokenizer_version` 写进 Qdrant collection metadata,启动时校验,
  防止 ETL 用 v1 词典灌库、检索时升级 v2 词典导致召回静默退化

WHY 单例而非 Provider 抽象:
- jieba 几 MB 内存零依赖,2C4G 也跑得动,不存在本地 vs API 双路径需求(§5.6.1)
- §2.3 Provider 抽象层只用于真正需要切换的组件,避免过度设计
"""
from __future__ import annotations

import hashlib
import logging
from functools import lru_cache
from pathlib import Path

log = logging.getLogger("infra.tokenizer")

# 词典路径相对 ai-service/ 根。生产 Docker 镜像把 knowledge/ 整个 COPY 进去
DICT_PATH = Path(__file__).resolve().parents[2] / "knowledge" / "dict" / "decoration_terms.txt"


class JiebaTokenizer:
    """单例分词器。首次 tokenize() 时 lazy load jieba 与词典,启动加速。"""

    def __init__(self) -> None:
        self._loaded = False
        self._jieba = None  # type: ignore[assignment]
        self._version: str = ""

    def _load(self) -> None:
        if self._loaded:
            return
        import jieba  # 延迟到第一次切词时才 import,启动 main.py 不阻塞
        self._jieba = jieba

        # WHY 关掉日志:jieba 默认会 print "Building prefix dict..." 到 stderr,污染服务日志
        jieba.setLogLevel(logging.WARN)

        # WHY load_userdict 后 jieba 把自定义词加入前缀树,优先整词切分
        if DICT_PATH.exists():
            jieba.load_userdict(str(DICT_PATH))
            log.info("loaded decoration dict: %s", DICT_PATH)
        else:
            # 词典还没产出(Sprint 1 早期),先走通用 jieba。后面 etl/extract_dict.py 产出后会生效
            log.warning("decoration dict not found, fall back to generic jieba: %s", DICT_PATH)

        self._version = self._compute_version()
        self._loaded = True
        log.info("jieba tokenizer ready, version=%s", self._version)

    def _compute_version(self) -> str:
        """version_tag = jieba 版本 + 词典文件 hash 的前 8 位。

        WHY 必须严格版本化:DESIGN §5.6.1 强制 ETL/查询用同一套分词;
        词典升级一行词都会导致 BM25 indices 漂移,检索召回断崖式下跌。
        """
        import jieba
        jieba_ver = getattr(jieba, "__version__", "unknown")
        dict_hash = "nodict"
        if DICT_PATH.exists():
            dict_hash = hashlib.sha256(DICT_PATH.read_bytes()).hexdigest()[:8]
        return f"jieba-{jieba_ver}+dict-{dict_hash}"

    def tokenize(self, text: str) -> list[str]:
        """精确模式切词,去掉空白与单字符标点。返回 term list。"""
        self._load()
        assert self._jieba is not None
        # WHY cut(HMM=False):带 HMM 会对未登录词做新词发现,可能切出我们没在词典里的"新词",
        # 导致 ETL 时词表与查询时不一致。装修域用纯词典精确匹配更稳。
        tokens = [t.strip() for t in self._jieba.cut(text, HMM=False)]
        return [t for t in tokens if len(t) > 0 and not t.isspace()]

    def to_sparse_vector(self, text: str) -> tuple[list[int], list[float]]:
        """切词 → (indices, values) for Qdrant SparseVector。

        WHY 用 hash 做 term→id:
        - 不需要维护全局词表(避免 ETL 与服务启动顺序耦合)
        - 32-bit hash 在装修领域 ~10K 候选词规模下碰撞可忽略
        - Qdrant 服务端 IDF 自动归一,values 直接给 tf 即可
        """
        tokens = self.tokenize(text)
        if not tokens:
            return [], []
        tf: dict[int, int] = {}
        for tok in tokens:
            tid = _stable_term_id(tok)
            tf[tid] = tf.get(tid, 0) + 1
        indices = list(tf.keys())
        values = [float(v) for v in tf.values()]
        return indices, values

    @property
    def version(self) -> str:
        self._load()
        return self._version


def _stable_term_id(term: str) -> int:
    """term → 32-bit 正整数 ID。md5 前 8 位转 int,稳定不依赖 Python hash seed。"""
    h = hashlib.md5(term.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


@lru_cache
def get_tokenizer() -> JiebaTokenizer:
    return JiebaTokenizer()
