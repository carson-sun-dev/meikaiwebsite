"""RAG 检索工具 — Sprint 2 step 5:从 quote_items_bge 拉 top-k 历史 line items 作为 L2 导购话术的"有据"参考。

DESIGN 锚点:
- §3 Sprint 2 step 5:Hybrid RAG 接入 SubGraph,让 L2 导购话术对照真实历史
- §5.6 Hybrid Search:Jieba 客户端 tokenize + RRF 服务端融合(走 qdrant_client.hybrid_search)
- §11.4 工程纪律:外部依赖(Qdrant)异常不阻断主流程,失败降级为空 list

WHY 不复用 quote 工具的统计兜底,而是单独做"案例检索":
- quote.py 给的是"档位区间 ¥/㎡",数字侧已合规
- RAG 给的是"案例素材"(具体项目里的 line item:门头、厨房、空调等),让 L2 说"我们之前
  也做过XX项目,门头大约用了 XX 工艺"这类有依据的导购话术 — 数字本身仍以 quote_block 为准
- 拆分两个数据来源:统计(quote_stats_per_sqm.json)→ 价格档位;向量库(quote_items_bge)→ 工艺案例

WHY business_line 过滤走 client-side 而非 Qdrant payload filter:
- quote_items_bge 的 payload 是 quotes.jsonl 的字段(item_name/spec/unit_price/...),
  没有 business_line — 业务线在 projects_labeled.jsonl(项目维度,不是 line item 维度)
- 重灌 Qdrant 加 business_line 字段是更"正确"的做法,但成本高(全量 re-index)
- 客户端通过 project_id → business_line 映射后过滤,成本低且足够过滤精度

WHY top_k 默认 3 而非 5:
- few-shot 内容塞进 L2 prompt 会吃 token,3 条已能给 L2 足够"佐证感";5 条让 prompt 膨胀且
  收益递减(L2 选 1-2 条复述就够导购话术用)

WHY 失败降级返回 []:
- RAG 不可用时,quote 工具产出的 quote_block 仍可独立形成完整报价(数字已经合规)
- RAG 是"锦上添花",不是必经路径 — DESIGN §15 graceful degradation
"""
from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

from app.infra.qdrant_client import COL_QUOTE, hybrid_search

# WHY TYPE_CHECKING:`app.graphs.__init__` 顶层 import subgraphs,subgraphs 又 import 本模块,
#     如果运行期从 app.graphs.state import BusinessLine 会触发循环。BusinessLine 只是
#     Literal 类型别名,用 TYPE_CHECKING 仅在静态分析时引入即可,运行期不依赖
if TYPE_CHECKING:
    from app.graphs.state import BusinessLine

log = logging.getLogger("tools.rag")

DEFAULT_LABELS_PATH = Path("data/projects_labeled.jsonl")

# WHY 过滤阈值:line items 里有大量 quantity/unit_price 都缺的"分组标题"行(parse_quotes
#     启发式表头探测的副产物)。upsert_quote_items 写入时已用 _is_group_header 过滤过,
#     但 ETL 演进版本里偶尔会有漏网,这里再做一道兜底:无 subtotal 也无 unit_price 的行直接丢
def _is_meaningful_item(payload: dict[str, Any]) -> bool:
    return bool(payload.get("subtotal") or payload.get("unit_price"))


@lru_cache(maxsize=1)
def _load_project_to_business_line(path: str = str(DEFAULT_LABELS_PATH)) -> dict[str, str]:
    """加载 project_id → business_line 映射 — 进程内 lru_cache 永久缓存。

    Sprint 1 灌库时 projects_labeled.jsonl 已有 23 条全量人工标注,与 quotes.jsonl 同源。
    """
    p = Path(path)
    if not p.exists():
        log.warning("projects_labeled.jsonl 不存在 (%s),RAG 跳过 business_line 过滤", p)
        return {}
    mapping: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        pid = rec.get("project_id")
        bl = rec.get("business_line")
        if pid and bl:
            mapping[pid] = bl
    log.info("loaded %d project→business_line mappings", len(mapping))
    return mapping


def _compose_query(user_msg: str, business_type: str | None, business_line: BusinessLine) -> str:
    """把检索 query 拼成"业态 + 用户消息" — 业态前置让 BM25/Embedding 双侧都拿到锚定信号。

    WHY 不把 area_sqm 拼进去:面积数字对语义检索几乎无信号(80 平和 200 平在 embedding 空间
        距离很近),反而可能挤掉真正有信号的工艺关键词。
    """
    bl_hint_map = {
        "storefront": "门面房 店铺",
        "office": "办公室 写字楼",
        "residential": "住宅 家装",
        "unknown": "",
    }
    parts = [business_type or "", bl_hint_map.get(business_line, ""), user_msg]
    return " ".join(p for p in parts if p).strip()


class QuoteExample(dict):
    """检索回的 line item 摘要 — dict 子类便于 JSON 序列化与日志打印。

    字段:item_name / spec / unit_price / subtotal / project_id / business_line / score
    """


async def retrieve_quote_examples(
    user_msg: str,
    business_line: BusinessLine,
    business_type: str | None = None,
    top_k: int = 3,
    *,
    candidate_multiplier: int = 4,
) -> list[QuoteExample]:
    """从 quote_items_bge 检索 top-k 与查询语义相关的历史 line items。

    流程:
    1. compose query(业态 + 业务线 hint + 用户消息)
    2. hybrid_search 拿 top_k * candidate_multiplier 条候选(留余量给过滤)
    3. 客户端按 project_id 过滤到目标 business_line(若映射可加载)
    4. 过滤掉无 subtotal/unit_price 的标题行
    5. 取前 top_k 返回

    任何异常(Qdrant 不可达、collection 不存在、embedding 失败)都降级为空 list,
    不应阻断 SubGraph 的报价分支。

    WHY candidate_multiplier=4:business_line 过滤可能砍掉大半候选;粗召回 4*top_k 留余量。
    """
    if not user_msg or not user_msg.strip():
        return []

    query = _compose_query(user_msg, business_type, business_line)
    log.debug("RAG query for %s/%s: %r", business_line, business_type, query[:60])

    try:
        raw = await hybrid_search(
            collection=COL_QUOTE,
            query=query,
            top_k=top_k * candidate_multiplier,
        )
    except Exception as e:
        # WHY catch-all:RAG 是 best-effort,任何下游(Qdrant、embedding、tokenizer)挂掉
        #     都不能让报价分支跟着挂 — 走"无 RAG 退化版"L2 prompt 即可
        log.warning("hybrid_search failed,RAG 降级为空:%s", e)
        return []

    proj_to_bl = _load_project_to_business_line()

    out: list[QuoteExample] = []
    for hit in raw:
        payload = hit.get("payload") or {}
        if not _is_meaningful_item(payload):
            continue

        pid = payload.get("project_id")
        item_bl = proj_to_bl.get(pid) if pid else None
        # WHY 映射缺失时不一棒打死:Sprint 1 的 projects_labeled.jsonl 与 quotes.jsonl 同源,
        #     生产里映射应该齐全;但开发期可能局部演进导致漏对,放过比误杀好
        if item_bl is not None and item_bl != business_line:
            continue

        out.append(QuoteExample(
            item_name=payload.get("item_name") or "",
            spec=payload.get("spec") or "",
            unit_price=payload.get("unit_price"),
            subtotal=payload.get("subtotal"),
            project_id=pid,
            business_line=item_bl,
            score=hit.get("score"),
        ))
        if len(out) >= top_k:
            break

    log.info(
        "RAG retrieved %d/%d examples for %s/%s",
        len(out), len(raw), business_line, business_type,
    )
    return out


def format_examples_for_prompt(examples: list[QuoteExample]) -> str:
    """把检索结果摘成 prompt 用的"参考案例"段 — 控制长度避免 prompt 膨胀。

    WHY 不把 subtotal 数字显式列出:Guardrail 输出侧只允许 quote_block 内的数字出现;
        examples 里的金额(如某项目门头 ¥38000)若被 L2 复述会被 Guardrail 判违规。
        所以这里只暴露"工艺类目 + 规格描述"作为话术素材,数字侧由 quote_block 兜底。
    """
    if not examples:
        return ""
    lines = []
    for i, ex in enumerate(examples, 1):
        bits = [ex.get("item_name") or ""]
        if ex.get("spec"):
            bits.append(str(ex["spec"]))
        # WHY 截断 60 字:个别 line item spec 写到 200+ 字(完整工艺说明),prompt 里没必要
        desc = " · ".join(b for b in bits if b)[:60]
        lines.append(f"  {i}. {desc}")
    return "\n".join(lines)
