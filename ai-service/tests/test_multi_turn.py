"""Sprint 2 step 6 multi-turn 端到端测试 — checkpointer 跨轮状态复用。

WHY 用 InMemorySaver 而非 MySQL:
- 单测零外部依赖(无 docker compose);InMemorySaver 实现同一 BaseCheckpointSaver 协议,
  跨轮行为与 MySQL 等价(都按 thread_id 持久化 state)
- 生产/CI mysql 路径在 docker-compose 集成测试里验证(Sprint 3 计划)

测试用例覆盖:
1. 槽位跨轮 monotonic 合并:轮1 抽到火锅店,轮2 只补 200 平 → 报价分支命中
2. Router 短路:轮2 不再调 L0 分类(已有 business_line=storefront)
3. is_quote_intent 单调锁定:轮1=True 后轮2 抽到 False 不该退回引导分支
4. 不同 thread_id 隔离:thread A 的槽位不应漏到 thread B
"""
from __future__ import annotations

import re

import pytest
from langgraph.checkpoint.memory import InMemorySaver

from app.graphs import build_graph
from app.graphs import router as router_mod
from app.graphs import slots as slots_mod
from app.graphs import subgraphs as sg_mod
from app.tools import rag as rag_mod


class StubLLM:
    name = "stub"

    def __init__(self, reply: str) -> None:
        self._reply = reply

    async def stream(self, msg: str, level: str = "l0"):  # noqa: ARG002
        for ch in self._reply:
            yield ch


class TrackingLLM:
    """记录每次 stream 调用次数 — 用于断言 router 是否被短路。"""

    name = "tracking"

    def __init__(self, reply: str) -> None:
        self._reply = reply
        self.calls = 0

    async def stream(self, msg: str, level: str = "l0"):  # noqa: ARG002
        self.calls += 1
        for ch in self._reply:
            yield ch


class QuoteBlockEchoLLM:
    name = "quote-echo"

    async def stream(self, msg: str, level: str = "l2"):  # noqa: ARG002
        m = re.search(r"<quote_block>\n(.*?)\n</quote_block>", msg, re.DOTALL)
        reply = m.group(1) if m else "[NO_QUOTE_BLOCK]"
        for ch in reply:
            yield ch


class PromptEchoLLM:
    name = "prompt-echo"

    async def stream(self, msg: str, level: str = "l2"):  # noqa: ARG002
        for ch in msg:
            yield ch


@pytest.fixture(autouse=True)
def _stub_rag(monkeypatch):
    """multi-turn 测试不验 RAG,默认空 list 避免触达 Qdrant。"""
    async def _empty(**_kw):
        return []
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _empty)


@pytest.fixture
def patch_llms(monkeypatch):
    def _patch(slots_llm, subgraph_llm, router_llm):
        monkeypatch.setattr(slots_mod, "get_llm_client", lambda: slots_llm)
        monkeypatch.setattr(sg_mod, "get_llm_client", lambda: subgraph_llm)
        monkeypatch.setattr(router_mod, "get_llm_client", lambda: router_llm)

    return _patch


async def _collect_deltas(graph, initial: dict, config: dict) -> tuple[str, dict]:
    """跑 graph.astream 并聚合 deltas + 收集 updates(用于断言 state)。"""
    deltas: list[str] = []
    last_updates: dict = {}
    async for mode, payload in graph.astream(
        initial,
        config=config,
        stream_mode=["updates", "custom"],
    ):
        if mode == "custom" and isinstance(payload, dict) and payload.get("kind") == "delta":
            deltas.append(payload.get("text", ""))
        elif mode == "updates" and isinstance(payload, dict):
            last_updates.update(payload)
    return "".join(deltas), last_updates


async def test_slots_persist_across_turns(patch_llms):
    """轮1 抽到火锅店 + 报价意图(无面积) → 引导分支;
       轮2 只补'200 平米' → checkpointer merge 出齐套槽位 → 报价分支命中。
    """
    saver = InMemorySaver()
    graph = build_graph(checkpointer=saver)
    config = {"configurable": {"thread_id": "thread-A"}}

    # ---- 轮 1:有业态 + 报价意图,缺面积 ----
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn1, _ = await _collect_deltas(
        graph, {"user_msg": "想开个火锅店,装修咋样"}, config,
    )
    assert "quote_block" not in turn1  # 引导分支
    assert "已知信息" in turn1
    assert "火锅店" in turn1

    # ---- 轮 2:用户只补面积 ----
    # slots_llm 模拟"短消息抽不到业态",只抽到 area_sqm
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": null}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn2, _ = await _collect_deltas(
        graph, {"user_msg": "200 平米"}, config,
    )

    # 关键断言:轮 2 命中报价分支(说明 merge 后槽位齐了)
    assert "基础档" in turn2, f"轮 2 应进入报价分支,得到:\n{turn2[:300]}"
    assert "中端档" in turn2
    assert "高端档" in turn2
    assert "这只是AI输出的价格" in turn2
    # 业态来自轮 1,面积来自轮 2 — 标题行二者皆有
    assert "200㎡" in turn2
    assert "火锅店" in turn2


async def test_router_short_circuits_on_followup(patch_llms):
    """轮 2 复用上一轮 business_line,不再调 router L0 LLM。"""
    saver = InMemorySaver()
    graph = build_graph(checkpointer=saver)
    config = {"configurable": {"thread_id": "thread-router"}}

    tracking_router = TrackingLLM("storefront")
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=tracking_router,
    )
    await _collect_deltas(graph, {"user_msg": "想开个火锅店"}, config)
    assert tracking_router.calls == 1, "轮 1 router 必须调一次 L0"

    # 轮 2:同 thread,router 应短路
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": null}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=tracking_router,  # 共用同一实例
    )
    await _collect_deltas(graph, {"user_msg": "200 平米"}, config)
    assert tracking_router.calls == 1, "轮 2 router 必须短路,不应再调 L0"


async def test_quote_intent_is_monotonic(patch_llms):
    """轮 1 is_quote_intent=True;轮 2 LLM 抽到 False 不应回退 — 用户问过价不能丢这个状态。"""
    saver = InMemorySaver()
    graph = build_graph(checkpointer=saver)
    config = {"configurable": {"thread_id": "thread-intent"}}

    # 轮 1:报价意图明确
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn1, _ = await _collect_deltas(
        graph, {"user_msg": "我开火锅店 200 平 多少钱"}, config,
    )
    assert "基础档" in turn1

    # 轮 2:用户追问"那中端档大概什么工艺?"(意图字段被本轮 LLM 抽成 false)
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": false, "area_sqm": null, "business_type": null}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn2, _ = await _collect_deltas(
        graph, {"user_msg": "那中端档大概什么工艺"}, config,
    )
    # 意图锁定 + 面积/业态 monotonic 保留 → 仍走报价分支
    assert "基础档" in turn2 or "中端档" in turn2, \
        f"is_quote_intent monotonic 应保持报价分支,得到:\n{turn2[:300]}"


async def test_threads_are_isolated(patch_llms):
    """thread A 的槽位不应漏到 thread B — checkpointer 必须按 thread_id 隔离 state。"""
    saver = InMemorySaver()
    graph = build_graph(checkpointer=saver)

    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    # thread A:报价
    await _collect_deltas(
        graph, {"user_msg": "我开火锅店 200 平 多少钱"},
        {"configurable": {"thread_id": "A"}},
    )

    # thread B:全新会话,只说"价格"(无业态/面积)
    # slots LLM 模拟"抽不到"
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": null}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn_b, _ = await _collect_deltas(
        graph, {"user_msg": "想咨询价格"},
        {"configurable": {"thread_id": "B"}},
    )

    # B 不应该看到 A 的火锅店/200 平 — 必须走引导分支
    assert "quote_block" not in turn_b, "thread B 不应继承 thread A 的槽位"
    assert "基础档" not in turn_b
    assert "已知信息" in turn_b


def test_merge_slots_pure_function():
    """_merge_slots 纯函数:核心合并规则的直接断言。"""
    merge = sg_mod._merge_slots

    # 已知 truthy 字段保留,新值若 falsy 不覆盖
    assert merge({"business_type": "火锅店"}, {"business_type": None}) == {"business_type": "火锅店"}
    assert merge({"area_sqm": 200}, {"area_sqm": 0}) == {"area_sqm": 200}

    # 新 truthy 值覆盖旧值(用户改主意)
    assert merge({"area_sqm": 200}, {"area_sqm": 250}) == {"area_sqm": 250}

    # is_quote_intent:True 锁定
    assert merge({"is_quote_intent": True}, {"is_quote_intent": False})["is_quote_intent"] is True
    # 之前没设 + 本轮抽到 False → 取本轮
    assert merge({}, {"is_quote_intent": False}) == {"is_quote_intent": False}
    # 之前没设 + 本轮 True → True
    assert merge({}, {"is_quote_intent": True}) == {"is_quote_intent": True}

    # prev=None 容忍
    assert merge(None, {"area_sqm": 100}) == {"area_sqm": 100}
    # new=None 容忍
    assert merge({"area_sqm": 100}, None) == {"area_sqm": 100}
