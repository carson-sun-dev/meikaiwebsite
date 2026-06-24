"""Router 节点 — 用 L0 LLM 把用户首条消息分类到三大业务线之一。

WHY 走 L0 而非 L2:
- 分类任务只需要"3 选 1 + 兜底 unknown",~10 token 输出
- L0(Doubao-Lite)成本是 L2(DeepSeek-V3.2)的 ~1/100,且延迟低
- 错误代价低:即使误分类,SubGraph 内部仍会用 L2 真正对话,Router 只是分流闸

WHY 在 LLM 输出再过一层关键词匹配,而不是约束 JSON schema:
- L0 模型对单词级输出格式遵从度足够,但偶尔会带前后引号/解释("storefront / 门面房")
- 关键词 in 字符串匹配比要求严格 JSON 更稳健,SubGraph 路由不会因为多了个标点而崩
- 找不到则 fallback storefront(美恺核心业务,降级最合理)
"""
from __future__ import annotations

import logging

from app.graphs.state import BusinessLine, ChatState
from app.infra.llm_client import get_llm_client

log = logging.getLogger("graphs.router")

# Sprint A 启发式兜底:用户消息明显含业务线词时直接判,跳过 L0
# 比 L0 更快 + 更稳(L0 对短消息"你好/120 平"会误判)
LINE_KEYWORDS = {
    "storefront": ("店铺", "门店", "门面", "餐饮", "火锅", "茶馆", "咖啡", "奶茶", "零售",
                   "美容", "服装", "饭店", "餐厅", "饮品", "外卖", "堂食", "店"),
    "office": ("办公", "写字楼", "公司", "团队", "工位", "会议室", "前台", "弱电"),
    "residential": ("家装", "住宅", "新房", "二手房", "翻新", "户型", "家里", "自己家",
                    "我家", "卧室", "客厅", "婚房", "学区房"),
}

ROUTER_PROMPT = """你是装修业态分类助手。根据用户首条消息判断他想装修的空间类型,只输出 1 个英文标签:

- residential:住宅家装(自住房、新房、二手房翻新、别墅、公寓内装)
- office:办公空间(写字楼、商务楼、学校办公楼、政企单位办公)
- storefront:门面房店铺(餐饮/火锅/茶馆/咖啡店/零售/服装/眼镜店/美容院/便利店等所有对外营业的实体店面)

只输出一个词:residential / office / storefront。不要解释,不要标点。

用户消息:{msg}
分类标签:"""


async def classify_node(state: ChatState) -> dict:
    """聚合 L0 流式输出 → 抠出 business_line 标签写回 state。"""
    user_msg = state.get("user_msg", "").strip()
    if not user_msg:
        log.warning("router got empty user_msg → unknown")
        return {"business_line": "unknown", "business_line_confident": False}

    existing = state.get("business_line")
    if existing and existing != "unknown":
        log.info("router short-circuit:复用上一轮 business_line=%s", existing)
        # 保留上轮 confident 状态(不在此覆盖,让 state 自然继承)
        return {"business_line": existing}

    # Sprint A 启发式:用户消息明显含业务线词 → 直接判,不调 LLM 更稳更快
    for biz, keywords in LINE_KEYWORDS.items():
        if any(kw in user_msg for kw in keywords):
            log.info("router heuristic %r → %s (kw match)", user_msg[:30], biz)
            return {"business_line": biz, "business_line_confident": True}

    # 启发式没命中 → L0 LLM 兜底
    llm = get_llm_client()
    full = ""
    async for chunk in llm.stream(ROUTER_PROMPT.format(msg=user_msg), level="l0"):
        full += chunk

    raw = full.strip().lower()
    for biz in ("residential", "office", "storefront"):
        if biz in raw:
            log.info("router classified %r → %s (raw=%r)", user_msg[:30], biz, full[:60])
            return {"business_line": biz, "business_line_confident": True}

    # Sprint A:LLM 也判不出 → 标 unknown + confident=False,让 chat 先问业务线
    # 之前 fallback storefront → 用户说"你好"被直接当成"想问店铺",导致 AI 假设业务线
    log.warning("router unable to classify,标 unknown 让 chat 先问业务线,raw=%r", full[:80])
    return {"business_line": "unknown", "business_line_confident": False}


def route_to_subgraph(state: ChatState) -> str:
    """conditional_edge 选择函数:返回节点名 = business_line。"""
    bl: BusinessLine = state.get("business_line", "storefront")  # type: ignore[assignment]
    # WHY unknown 兜底走 storefront:美恺核心业务,默认承接最不会出洋相
    if bl == "unknown":
        return "storefront"
    return bl
