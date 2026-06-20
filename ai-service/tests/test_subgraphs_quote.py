"""SubGraph 报价分支端到端测试 — slots 齐 → quote 工具 → L2 prompt 含 quote_block。

WHY 跑完整 graph.astream 而非直接调 node 函数:
- subgraph node 内部用 get_stream_writer(),只在 LangGraph 节点 context 才可用
- 端到端跑通也顺带验证 router → subgraph 拓扑、stream_mode='custom' 协议

测试策略:
- patch slots/subgraphs/router 三处的 get_llm_client 各自返回 StubLLM
- 报价分支:让 L2 stub 把 prompt 里的 <quote_block> 内容回吐,断言最终 delta 含 DISCLAIMER + 三档
- 引导分支:让 L2 stub 直接 echo 整个 prompt,断言 prompt 不含 quote_block 但含"已知信息"
"""
from __future__ import annotations

import re

import pytest

from app.graphs import slots as slots_mod
from app.graphs import subgraphs as sg_mod
from app.graphs import router as router_mod
from app.graphs import get_graph
from app.tools import rag as rag_mod


@pytest.fixture(autouse=True)
def _disable_rag_by_default(monkeypatch):
    """默认禁用 RAG(返回 [])避免现有测试触达真 Qdrant;需要时单测内重新 patch。"""
    async def _empty(**_kw):
        return []
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _empty)


class StubLLM:
    name = "stub"

    def __init__(self, reply: str) -> None:
        self._reply = reply

    async def stream(self, msg: str, level: str = "l0"):  # noqa: ARG002
        for ch in self._reply:
            yield ch


class QuoteBlockEchoLLM:
    """从 prompt 中抠 <quote_block>...</quote_block> 内容回吐 — 模拟 L2 严格遵守规则。"""

    name = "quote-echo"

    async def stream(self, msg: str, level: str = "l2"):  # noqa: ARG002
        m = re.search(r"<quote_block>\n(.*?)\n</quote_block>", msg, re.DOTALL)
        reply = m.group(1) if m else "[NO_QUOTE_BLOCK]"
        for ch in reply:
            yield ch


class PromptEchoLLM:
    """整 prompt 回吐 — 测试可断言 prompt 结构。"""

    name = "prompt-echo"

    async def stream(self, msg: str, level: str = "l2"):  # noqa: ARG002
        for ch in msg:
            yield ch


class HallucinateLLM:
    """模拟 L2 编造金额且漏写 DISCLAIMER — 用于触发 Guardrail 覆盖。"""

    name = "hallucinate"

    async def stream(self, msg: str, level: str = "l2"):  # noqa: ARG002
        reply = "好的,我帮您算下:门面房 200 平,差不多 ¥99999/㎡,整套 ¥19,999,800,赶紧定。"
        for ch in reply:
            yield ch


@pytest.fixture
def patch_llms(monkeypatch):
    """工厂:分别 patch slots / subgraphs / router 三处的 get_llm_client。"""

    def _patch(slots_llm, subgraph_llm, router_llm):
        monkeypatch.setattr(slots_mod, "get_llm_client", lambda: slots_llm)
        monkeypatch.setattr(sg_mod, "get_llm_client", lambda: subgraph_llm)
        monkeypatch.setattr(router_mod, "get_llm_client", lambda: router_llm)

    return _patch


async def _collect_deltas(graph, initial: dict) -> str:
    """跑 graph.astream 并聚合所有 custom delta 文本。"""
    deltas = []
    async for mode, payload in graph.astream(initial, stream_mode=["updates", "custom"]):
        if mode == "custom" and isinstance(payload, dict) and payload.get("kind") == "delta":
            deltas.append(payload.get("text", ""))
    return "".join(deltas)


async def test_storefront_quote_branch_streams_quote_block(patch_llms):
    """火锅店 200 平米 → 槽位齐 → estimate_storefront_quote → L2 输出含 DISCLAIMER + 三档。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我开个火锅店 200 平米要多少钱"},
    )

    # quote_block 内必含三档与免责声明
    assert "基础档" in full
    assert "中端档" in full
    assert "高端档" in full
    assert "这只是AI输出的价格" in full
    assert "美恺装饰" in full
    # 200㎡ 出现在 format_quote_for_chat 的标题行
    assert "200㎡" in full


async def test_office_quote_branch_uses_industry_default(patch_llms):
    """办公 80 平 → 走 industry_default:office,新口径下显示价 ¥700-900。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 80, "business_type": null}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("office"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我有个办公室 80 平米想装修,多少钱"},
    )

    assert "办公空间" in full
    # 验证新口径(2026-06-09 店主锚定值):显示价至少出现 700 或 900 这种关键数字
    assert "700" in full or "800" in full or "900" in full
    assert "这只是AI输出的价格" in full


async def test_chat_branch_when_area_missing(patch_llms):
    """没有面积 → 走引导分支,prompt 不含 quote_block,但包含'已知信息'与已抽业态。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),  # 直接 echo prompt 便于断言
        router_llm=StubLLM("storefront"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "想开个火锅店,装修咋样"},
    )

    assert "quote_block" not in full  # 引导分支不带 quote_block 标签
    assert "已知信息" in full
    assert "火锅店" in full  # 已抽到的业态注入 prompt


async def test_chat_branch_when_intent_false(patch_llms):
    """has area 但 is_quote_intent=False(纯闲聊) → 引导分支。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": false, "area_sqm": 100, "business_type": null}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("residential"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我家 100 平,你们有什么服务"},
    )

    assert "quote_block" not in full
    assert "已知信息" in full


async def test_guardrail_appends_authoritative_when_llm_hallucinates(patch_llms):
    """L2 编造 ¥99999 且漏写 DISCLAIMER → Guardrail 在 SSE 末尾追加权威报价段。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=HallucinateLLM(),
        router_llm=StubLLM("storefront"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我开个火锅店 200 平米要多少钱"},
    )

    # L2 编造的原文先流给了用户
    assert "99999" in full
    # Guardrail 追加的权威段标记 + format_quote_for_chat 关键内容
    assert "系统校准" in full
    assert "基础档" in full
    assert "中端档" in full
    assert "高端档" in full
    assert "这只是AI输出的价格" in full


async def test_quote_tool_failure_falls_back_to_chat(patch_llms, monkeypatch):
    """报价工具异常 → 降级到引导分支,不应让 SSE 流崩。"""
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )

    def _raise(*_a, **_kw):
        raise RuntimeError("simulated quote tool failure")

    monkeypatch.setitem(sg_mod.QUOTE_FN, "storefront", _raise)

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我开个火锅店 200 平米要多少钱"},
    )

    # 降级到 chat 分支:不含 quote_block,但应有引导话术 prompt 结构
    assert "quote_block" not in full
    assert "已知信息" in full


# ---- Sprint 2 step 5 RAG 集成 ----

async def test_quote_branch_injects_rag_examples_into_prompt(monkeypatch, patch_llms):
    """RAG 命中 → quote prompt 含【历史案例参考】段 + 案例 item_name。"""

    async def _fake_rag(**_kw):
        return [
            rag_mod.QuoteExample(
                item_name="门头招牌制作", spec="3M 灯箱布 + 内打光",
                subtotal=38000, unit_price=None,
                project_id="proj_X", business_line="storefront", score=0.9,
            ),
            rag_mod.QuoteExample(
                item_name="厨房排烟系统", spec="304 不锈钢风管 + 油烟净化",
                subtotal=25000, unit_price=None,
                project_id="proj_Y", business_line="storefront", score=0.85,
            ),
        ]
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _fake_rag)

    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),  # echo 整 prompt 便于断言
        router_llm=StubLLM("storefront"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我开火锅店 200 平米多少钱"},
    )

    # prompt 段含案例标题 + 工艺类目
    assert "历史案例参考" in full
    assert "门头招牌制作" in full
    assert "厨房排烟系统" in full
    # WHY 金额绝不能出现在 prompt 段:Guardrail 只允许 quote_block 内的数字
    assert "38000" not in full.split("</quote_block>")[0].split("<quote_block>")[0]
    assert "25000" not in full.split("</quote_block>")[0].split("<quote_block>")[0]
    # 严格规则第 5 条触发
    assert "严禁复述案例里的任何金额" in full


async def test_quote_branch_still_works_when_rag_fails(monkeypatch, patch_llms):
    """RAG 抛异常时 SubGraph 不应崩,报价分支仍能产出 quote_block。

    WHY 测这条:rag.py 内部已 catch-all 降级,这里防止以后有人误把 try/except 删了 —
        SubGraph 报价路径对 RAG 必须是"有则锦上添花,无则照常"。
    """

    async def _boom(**_kw):
        raise RuntimeError("simulated RAG outage")
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _boom)

    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )

    # _collect_deltas 不应抛 — 应该完整流完并含三档报价
    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "我开个火锅店 200 平米要多少钱"},
    )

    assert "基础档" in full
    assert "中端档" in full
    assert "高端档" in full
    assert "这只是AI输出的价格" in full


async def test_rag_examples_not_injected_in_chat_branch(monkeypatch, patch_llms):
    """缺面积 → 走引导分支 → 不应调 RAG(节省 Qdrant 调用 + prompt 里不能含历史案例段)。"""
    rag_called = {"n": 0}

    async def _spy_rag(**_kw):
        rag_called["n"] += 1
        return []
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _spy_rag)

    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )

    full = await _collect_deltas(
        get_graph(),
        {"user_msg": "想开个火锅店,装修咋样"},
    )

    assert rag_called["n"] == 0, "引导分支不应触发 RAG"
    assert "历史案例参考" not in full
