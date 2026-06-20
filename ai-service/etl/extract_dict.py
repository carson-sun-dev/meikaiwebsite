"""
从 data/quotes.jsonl 抽取两份词典:

1. knowledge/dict/decoration_terms.txt — Jieba BM25 用 (~300 词)
   来源:line item 的 item_name + spec + category + remark 字段
   规则:含 ≥1 个中文字、长度 ≥2 字、TF ≥ 2 次、去掉纯数字与单位词

2. knowledge/dict/intent_keywords.txt — Guardrail §5.7.3 输入分类 Cascade Stage1 用 (~80 词)
   来源:decoration_terms 高频前 N + 手工种子(业态/空间/报价类)
   作用:用户首条消息若命中任一关键词,直接放行进 LangGraph 主流程,
        不调 L0 LLM 分类器,省 80% 的意图分类成本

用法:
    python -m etl.extract_dict --quotes data/quotes.jsonl

WHY 不直接用 LLM 自动总结:
- 词典是 ETL/查询一致性的契约(DESIGN §5.6.1),版本必须可复现
- LLM 总结每次结果不同,会导致 tokenizer_version 漂移
- 启发式 + 人工校对的产出可 diff 可 review
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from collections import Counter
from pathlib import Path

log = logging.getLogger("etl.extract_dict")

# WHY 这些种子词手工固化:
# - 业态:Router 分流 + 意图分类用,必须命中
# - 空间:用户常说"我家厨房想做..."等,LLM 槽位填充靠这些
# - 报价:Guardrail §5.7.3 信号④"含报价词+槽位不全"用,识别"问钱"意图
INTENT_SEED_KEYWORDS = {
    # 业态(三大业务线 + 常见细分)
    "装修", "装饰", "家装", "工装", "商装",
    "住宅", "新房", "二手房", "婚房", "学区房", "别墅",
    "办公室", "写字楼", "办公", "工位",
    "门面", "店铺", "商铺", "门头",
    "火锅店", "餐厅", "餐饮", "咖啡店", "茶馆", "茶饮", "奶茶店", "生煎", "饸饹",
    "眼镜店", "服装店", "美容院", "理发店", "便利店",
    "学校", "教室", "餐厅",
    # 空间
    "客厅", "卧室", "厨房", "卫生间", "浴室", "阳台", "书房", "餐厅", "玄关",
    "前厅", "后厨", "包间", "吧台", "收银台", "操作间",
    # 报价/咨询意图
    "价格", "报价", "预算", "多少钱", "几个钱", "造价", "费用", "成本",
    "便宜", "划算", "贵", "免费", "优惠",
    # 关键工艺词(高复用 + 客户口语)
    "吊顶", "地砖", "墙砖", "瓷砖", "刷漆", "乳胶漆", "水电", "水电改造",
    "防水", "贴砖", "踢脚线", "门窗", "橱柜", "衣柜", "整装", "半包", "全包",
    # 单位 / 规模(常和"多少钱"共现)
    "平米", "平方", "平方米", "㎡", "面积",
}

# Excel 报价单里常见的非术语噪声(单位词、虚词等),从装修词典中剔除
NOISE_WORDS = {
    "数量", "单价", "合价", "金额", "小计", "总计", "合计", "备注", "说明",
    "项目", "名称", "类别", "分类", "规格", "型号",
    "元", "米", "件", "套", "个", "块", "条", "张", "扇", "组", "项",
    "厘米", "毫米", "公斤", "千克", "克",
}

CN_CHAR_RE = re.compile(r"[一-鿿]")
ONLY_DIGIT_OR_PUNCT_RE = re.compile(r"^[\d\s\.,\-_/\\()\[\]【】（）+×*x:：;；'\"!?。、|]+$")


def is_candidate(term: str) -> bool:
    """词典候选筛选:长度 2-8、含中文、非纯数字/单位/噪声。"""
    t = term.strip()
    if not (2 <= len(t) <= 8):
        return False
    if not CN_CHAR_RE.search(t):
        return False
    if ONLY_DIGIT_OR_PUNCT_RE.match(t):
        return False
    if t in NOISE_WORDS:
        return False
    return True


def split_compound(text: str) -> list[str]:
    """初切:按常见分隔符 + 括号注释拆开。

    举例:"瓷砖(800×800 抛光)" → ["瓷砖", "800×800 抛光"]
    这里只做粗切,Jieba 还会做二次细切——但我们要的是"作为整体出现过"的词组,
    所以保留粗切片段加进候选,再用频率过滤。
    """
    # 去括号内容(连同括号),再按常见分隔符拆
    cleaned = re.sub(r"[（(\[【].*?[)）\]】]", " ", text)
    parts = re.split(r"[\s,，;；/|+×*x、:：]+", cleaned)
    return [p.strip() for p in parts if p.strip()]


def extract_decoration_terms(quotes_path: Path, min_tf: int = 2, top_n: int = 350) -> list[tuple[str, int]]:
    """扫 quotes.jsonl,从 item_name / spec / category / remark 抽候选词,按 TF 排序。

    WHY min_tf=2:出现 1 次的词大概率是脏数据或一次性条目,留下噪声;
                  门槛 2 已经能压住绝大多数误抽。
    """
    counter: Counter[str] = Counter()
    for line in quotes_path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        for field in ("item_name", "spec", "category", "remark"):
            text = rec.get(field) or ""
            for piece in split_compound(text):
                if is_candidate(piece):
                    counter[piece] += 1

    return [(w, c) for w, c in counter.most_common(top_n * 3) if c >= min_tf][:top_n]


def write_jieba_dict(terms: list[tuple[str, int]], path: Path) -> None:
    """Jieba userdict 格式:`词 词频 [词性]`,一行一条。

    WHY 词频用真实 TF(而非 hardcoded 大数):
    词频反映领域强度,Jieba 在歧义切分时会偏向词频高的方案,
    自然带"装修域语言模型"效果。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# 自动生成,来源:23 份历史报价单 item_name/spec/category/remark 字段\n")
        f.write("# 格式:词 词频 [词性可省]\n")
        f.write("# 重灌请删除后重跑 `python -m etl.extract_dict`\n")
        for term, tf in terms:
            f.write(f"{term} {tf} n\n")


def write_intent_keywords(decoration_terms: list[tuple[str, int]], path: Path) -> None:
    """意图关键词 = 种子词 ∪ 装修词典 top-N。

    WHY 与 decoration_terms 分离:
    - decoration_terms 用于 BM25 分词(召回率优先,词多一点没事)
    - intent_keywords 用于"是否进入主流程"的快速判定(精度优先,过宽会放行无关流量)
    所以这里只取装修词典前 50 词与种子词合并,共约 ~80-100 词。
    """
    merged = set(INTENT_SEED_KEYWORDS) | {t for t, _ in decoration_terms[:50]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Guardrail §5.7.3 输入分类 Cascade Stage1 关键词词典\n")
        f.write("# 命中任一关键词 → 直接进 LangGraph 主流程,不调 L0 LLM 分类\n")
        f.write("# 来源:手工种子 + decoration_terms.txt 前 50 词\n")
        for word in sorted(merged):
            f.write(f"{word}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", default="data/quotes.jsonl")
    ap.add_argument("--dict-out", default="knowledge/dict/decoration_terms.txt")
    ap.add_argument("--intent-out", default="knowledge/dict/intent_keywords.txt")
    ap.add_argument("--top-n", type=int, default=350, help="装修词典最多保留多少条")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    quotes_path = Path(args.quotes)
    if not quotes_path.exists():
        log.error("quotes file not found: %s; 先跑 python -m etl.parse_quotes", quotes_path)
        raise SystemExit(2)

    terms = extract_decoration_terms(quotes_path, top_n=args.top_n)
    log.info("extracted %d decoration terms (min_tf=2)", len(terms))

    write_jieba_dict(terms, Path(args.dict_out))
    log.info("wrote decoration dict → %s", args.dict_out)

    write_intent_keywords(terms, Path(args.intent_out))
    log.info("wrote intent keywords → %s", args.intent_out)

    log.info("top 20 decoration terms preview: %s", [t for t, _ in terms[:20]])


if __name__ == "__main__":
    main()
