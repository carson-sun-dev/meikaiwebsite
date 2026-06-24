"""LangGraph State 定义 — Sprint 2 起所有节点共享的对话状态。

WHY TypedDict total=False 而非 Pydantic BaseModel:
- LangGraph node return 部分字段(diff)合并到 state,total=False 允许节点只返回它修改的字段
- Pydantic 强类型在 LangGraph 0.2.x 与 diff-merge 配合略繁琐(每次部分返回都得 model_dump(exclude_unset))
- TypedDict 走的是字典,langgraph 直接 dict.update;字段语义靠注释 + Literal 守住即可

DESIGN §3 Sprint 2 槽位字段未来扩展:
- 家装(residential):area_sqm / room_count / budget_tier
- 办公(office):area_sqm / seat_count / weak_current(弱电)
- 门面房(storefront):biz_subtype(火锅/茶馆/...) / area_sqm / tier
"""
from __future__ import annotations

from typing import Any, Literal, TypedDict

BusinessLine = Literal["residential", "office", "storefront", "unknown"]


class ChatState(TypedDict, total=False):
    # 会话标识:Sprint 2 后期接 MySQL checkpointer 时作 thread_id
    conversation_id: str

    # 当轮用户输入(本 step 1 stub:每轮一句话,Sprint 2 后期改 messages list 支持多轮)
    user_msg: str

    # Router 输出 — 业态分流字段
    business_line: BusinessLine
    # Sprint A:business_line 是否"真识别"还是"兜底猜":
    # - True:LLM/正则确认了业务线 → chat 可以直接进 line-specific 流程
    # - False:用户消息无业务线信号,router 兜底了 → chat 应先问业务线再深入
    business_line_confident: bool

    # 业务槽位(SubGraph 内 extract_slots 节点填充:is_quote_intent / area_sqm / business_type;
    #         Sprint 2 step 6 multi-turn 接入后将跨轮复用,避免重复追问)
    slots: dict[str, Any]

    # 报价工具产物(quote.QuoteResult 字典);仅在槽位齐 + 报价意图命中时填充,否则缺席
    # WHY 落 state:Guardrail(step 4)需要原始 quote 与 LLM 输出做数字一致性反查
    quote: dict[str, Any]

    # Sprint 2 step 5 RAG 检索回的 top-k 历史 line item 摘要(参考案例)
    # WHY 落 state:便于评测/调试时回溯"L2 看到了哪些案例素材",也方便 step 6 multi-turn 跨轮复用
    rag_examples: list[dict[str, Any]]

    # 当前轮 LLM 最终聚合文本(SSE 通过 stream_writer 推 token,这里仅做日志/评测用途的快照)
    final_text: str
