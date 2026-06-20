"""
Qdrant 封装:Hybrid Search(稠密 Embedding + Jieba BM25,服务端 RRF 融合)。

DESIGN §5.6.1 关键决策(2026-06-01 Round 2):
- BM25 走 **Jieba 客户端预 tokenize**,不用 Qdrant 服务端 ICU 分词
  原因:ICU 对装修垂直术语(踢脚线/吊顶/水电铺设)切碎成单字,召回率断崖式下跌
- collection metadata 写入 `tokenizer_version`,启动时校验
  防止 ETL 用 v1 词典灌库、查询时升级 v2 词典导致 BM25 indices 漂移、检索静默退化
- IDF 仍由 Qdrant 服务端自动算(SparseVectorParams modifier=IDF)

Collection 命名(DESIGN §2.5 双路径维度兼容):
- knowledge_faq_bge:FAQ + 行业术语(bge-m3 1024d)
- quote_items_bge :历史报价 line items(bge-m3 1024d)
- 切到 Doubao 时改 collection 后缀 _doubao,ETL 重灌,业务代码不动
"""
from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qm

from app.config import get_settings
from app.infra.embedding import DENSE_DIM, get_embedding_client
from app.infra.tokenizer import get_tokenizer

log = logging.getLogger("infra.qdrant")

# WHY 名字带 provider 后缀:DESIGN §2.5 不同 embedding 维度不兼容,collection 物理隔离
# Sprint 1 默认本地完整版主路径 = bge-m3,后缀 _bge
COL_FAQ = "knowledge_faq_bge"
COL_QUOTE = "quote_items_bge"

DENSE_VEC = "dense"     # 命名向量,便于以后多向量扩展
SPARSE_VEC = "bm25"     # Jieba 客户端 token 化后的稀疏向量

# Payload 元数据键名(写在 Qdrant 服务端的 collection 配置 / 第一条 point 里)
META_TOKENIZER_VERSION = "_tokenizer_version"


def _client() -> AsyncQdrantClient:
    s = get_settings()
    return AsyncQdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key or None)


# ---------- 初始化 ----------

async def ensure_collections() -> None:
    """幂等创建两个 collection。已存在则校验 tokenizer_version 一致,不一致直接报错。

    WHY 拒绝写入而非自动重灌:
    - 静默重灌 = 静默丢数据,运维事故风险大
    - 应该由人决策:要么 drop 重灌(开发期),要么用旧版词典(线上)
    """
    cli = _client()
    tokenizer = get_tokenizer()
    current_ver = tokenizer.version

    existing = {c.name for c in (await cli.get_collections()).collections}

    common_kwargs = dict(
        vectors_config={DENSE_VEC: qm.VectorParams(size=DENSE_DIM, distance=qm.Distance.COSINE)},
        # WHY modifier=IDF:让 Qdrant 服务端在打分时按文档频率自动惩罚常见词(de, le, 装修域里"一二层"这种)
        sparse_vectors_config={SPARSE_VEC: qm.SparseVectorParams(modifier=qm.Modifier.IDF)},
    )

    for col in (COL_FAQ, COL_QUOTE):
        if col in existing:
            await _verify_tokenizer_version(cli, col, current_ver)
            log.info("collection exists & version verified: %s", col)
            continue
        await cli.create_collection(collection_name=col, **common_kwargs)
        # WHY 用一个 sentinel point 存版本:Qdrant 没有原生 collection metadata API,
        # 用 ID=0 的"哨兵 point"携带 _tokenizer_version 字段,后续查询时过滤掉
        await cli.upsert(
            collection_name=col,
            points=[qm.PointStruct(
                id=0,
                vector={DENSE_VEC: [0.0] * DENSE_DIM, SPARSE_VEC: qm.SparseVector(indices=[0], values=[0.0])},
                payload={META_TOKENIZER_VERSION: current_ver, "_sentinel": True},
            )],
        )
        log.info("created collection %s (tokenizer_version=%s)", col, current_ver)


async def _verify_tokenizer_version(cli: AsyncQdrantClient, col: str, expect: str) -> None:
    """读取 ID=0 sentinel point,比对 tokenizer_version。不一致直接抛错。"""
    points = await cli.retrieve(collection_name=col, ids=[0], with_payload=True)
    if not points:
        log.warning("collection %s has no sentinel point — 旧数据?跳过版本校验", col)
        return
    stored = points[0].payload.get(META_TOKENIZER_VERSION) if points[0].payload else None
    if stored != expect:
        raise RuntimeError(
            f"tokenizer_version mismatch on '{col}': stored={stored} expect={expect}\n"
            f"  → 词典已升级,需要 drop 重灌:cli.delete_collection('{col}') 后重跑 ETL"
        )


# ---------- 写入 ----------

async def upsert_quote_items(items: Iterable[dict[str, Any]]) -> int:
    """items: ETL 产出的 line item dict;返回写入条数。

    WHY 跳过 quantity & unit_price 都为 None 的行:
    parse_quotes 的启发式表头探测会把分组标题(如"大厅装修")也当 line item 抓进来,
    这些行没有真实数量/单价,作为检索语料反而是噪音(query "大厅装修多少钱"会优先命中标题,
    但标题本身没有金额信息,无法回答)。
    """
    embed = get_embedding_client()
    tok = get_tokenizer()
    cli = _client()

    batch = [it for it in items if not _is_group_header(it)]
    if not batch:
        return 0

    texts = [_compose_text_for_quote(it) for it in batch]
    dense = await embed.embed(texts)

    points = []
    for i, (it, d) in enumerate(zip(batch, dense)):
        indices, values = tok.to_sparse_vector(texts[i])
        points.append(qm.PointStruct(
            id=_stable_id(it),
            vector={
                DENSE_VEC: d,
                SPARSE_VEC: qm.SparseVector(indices=indices, values=values),
            },
            payload={**it, "_text": texts[i]},
        ))

    await cli.upsert(collection_name=COL_QUOTE, points=points)
    return len(points)


def _is_group_header(it: dict[str, Any]) -> bool:
    return it.get("quantity") is None and it.get("unit_price") is None and it.get("subtotal") is None


def _compose_text_for_quote(it: dict[str, Any]) -> str:
    """把 line item 拼成单段检索文本。

    WHY 拼 raw_row 里的"工艺说明":parse_quotes 没把"工艺做法及材料说明"映射到结构化字段
    (列名不在 COLUMN_ALIASES 里),但它的语义价值最高(详见 §5.6 检索文本组织)。
    这里从 raw_row 兜底捞一次。
    """
    parts = [
        it.get("item_name") or "",
        it.get("spec") or "",
        it.get("category") or "",
        it.get("remark") or "",
    ]
    raw = it.get("raw_row") or {}
    for k, v in raw.items():
        if "说明" in str(k) or "做法" in str(k) or "工艺" in str(k):
            if v and str(v).lower() != "nan":
                parts.append(str(v))
    return " ".join(p for p in parts if p).strip()


def _stable_id(it: dict[str, Any]) -> int:
    """确定性 ID,便于重复 ETL 幂等。基于 project + sheet + row。"""
    import hashlib
    # WHY 从 1 起(0 被 sentinel point 占),避免 ETL 写入覆盖版本哨兵
    key = f"{it.get('project_id')}|{it.get('sheet')}|{it.get('row_idx')}"
    h = int(hashlib.md5(key.encode()).hexdigest()[:15], 16)
    return max(h, 1)


# ---------- 检索:Hybrid + RRF ----------

async def hybrid_search(
    collection: str,
    query: str,
    top_k: int = 5,
    filter_payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """单次调用走 Qdrant Query API 的 Reciprocal Rank Fusion(无需手动融合)。

    需要 qdrant-client ≥ 1.10。
    """
    embed = get_embedding_client()
    tok = get_tokenizer()
    cli = _client()
    dense = (await embed.embed([query]))[0]
    sparse_idx, sparse_val = tok.to_sparse_vector(query)

    # WHY 过滤掉 sentinel point:_sentinel=True 不应出现在用户检索结果中
    qfilter = _build_filter(filter_payload, exclude_sentinel=True)

    res = await cli.query_points(
        collection_name=collection,
        prefetch=[
            qm.Prefetch(query=dense, using=DENSE_VEC, limit=top_k * 4),
            qm.Prefetch(
                query=qm.SparseVector(indices=sparse_idx, values=sparse_val),
                using=SPARSE_VEC, limit=top_k * 4,
            ),
        ],
        query=qm.FusionQuery(fusion=qm.Fusion.RRF),
        query_filter=qfilter,
        limit=top_k,
        with_payload=True,
    )
    return [{"score": p.score, "payload": p.payload} for p in res.points]


def _build_filter(payload: dict[str, Any] | None, *, exclude_sentinel: bool = True) -> qm.Filter:
    must = []
    must_not = []
    if payload:
        must = [qm.FieldCondition(key=k, match=qm.MatchValue(value=v)) for k, v in payload.items()]
    if exclude_sentinel:
        must_not.append(qm.FieldCondition(key="_sentinel", match=qm.MatchValue(value=True)))
    return qm.Filter(must=must or None, must_not=must_not or None)
