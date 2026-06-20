"""slots.extract_slots 单测 — 覆盖 LLM JSON / markdown 围栏 / 解析失败 / LLM 异常 四种形态。

WHY 测 LLM 输出畸形而非只测 happy path:
- L0 模型对单字段输出鲁棒,但 JSON 输出常带 markdown 围栏、前后解释、单引号、null→"null"
- 正则兜底是 DESIGN §11.4 工程纪律的体现,必须验证"LLM 完全失败时关键字段仍能落"
"""
from __future__ import annotations

import pytest

from app.graphs import slots as slots_mod


class StubLLM:
    """逐字回放固定字符串的最小 LLMClient — 不消耗 token,不接网络。"""

    name = "stub"

    def __init__(self, reply: str) -> None:
        self._reply = reply

    async def stream(self, msg: str, level: str = "l0"):  # noqa: ARG002
        for ch in self._reply:
            yield ch


class FailLLM:
    """每次调用 stream 立即抛 RuntimeError,模拟网络/鉴权异常。"""

    name = "fail"

    async def stream(self, msg: str, level: str = "l0"):  # noqa: ARG002
        raise RuntimeError("boom")
        yield  # pragma: no cover  让 python 识别为 async generator


@pytest.fixture
def patch_llm(monkeypatch):
    """工厂:传入 LLMClient 实例,patch slots 模块里的 get_llm_client。"""

    def _patch(client):
        monkeypatch.setattr(slots_mod, "get_llm_client", lambda: client)

    return _patch


async def test_pure_json_happy_path(patch_llm):
    patch_llm(StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'))
    s = await slots_mod.extract_slots("我开个火锅店 200 平米要多少钱", "storefront")
    assert s["is_quote_intent"] is True
    assert s["area_sqm"] == 200.0
    assert s["business_type"] == "火锅店"


async def test_markdown_fence_stripped(patch_llm):
    """LLM 输出带 ```json ... ``` 围栏也应解析成功。"""
    patch_llm(StubLLM('```json\n{"is_quote_intent": true, "area_sqm": 80, "business_type": null}\n```'))
    s = await slots_mod.extract_slots("办公室 80 平", "office")
    assert s["area_sqm"] == 80.0
    assert s["is_quote_intent"] is True
    # business_type=null,且消息正则也没命中 office 业态(列表里没"办公室"),应缺席
    assert "business_type" not in s


async def test_json_with_preamble(patch_llm):
    """LLM 在 JSON 前加了解释文字,_parse_llm_json 应取最外层 {...}。"""
    patch_llm(StubLLM('好的,提取结果如下:{"is_quote_intent": false, "area_sqm": null, "business_type": null}'))
    s = await slots_mod.extract_slots("你好", "storefront")
    assert s["is_quote_intent"] is False
    assert "area_sqm" not in s


async def test_llm_garbage_heuristic_takes_over(patch_llm):
    """LLM 完全不输出 JSON,正则应抠出面积 + 意图。"""
    patch_llm(StubLLM("抱歉我不太理解"))
    s = await slots_mod.extract_slots("装修我家 90 平米要多少钱", "residential")
    assert s["area_sqm"] == 90.0
    assert s["is_quote_intent"] is True  # "多少钱" 命中关键词


async def test_llm_exception_pure_heuristic(patch_llm):
    """LLM stream 抛异常,纯走正则,业务不应崩。"""
    patch_llm(FailLLM())
    s = await slots_mod.extract_slots("我开个茶馆 150 平米,预算大概多少", "storefront")
    assert s["area_sqm"] == 150.0
    assert s["business_type"] == "茶馆"
    assert s["is_quote_intent"] is True  # "预算" 命中


async def test_business_type_long_match_first(patch_llm):
    """火锅店 必须在 饭店/店 之前匹配,不能抽成 "饭店" 或其他。"""
    patch_llm(FailLLM())  # 走纯正则
    s = await slots_mod.extract_slots("我开个火锅店", "storefront")
    assert s["business_type"] == "火锅店"


async def test_null_string_business_type_filtered(patch_llm):
    """LLM 把 null 错输成字符串 'null' 应被过滤,不能成为 business_type='null'。"""
    patch_llm(StubLLM('{"is_quote_intent": false, "area_sqm": null, "business_type": "null"}'))
    s = await slots_mod.extract_slots("hello", "storefront")
    assert "business_type" not in s
    assert "area_sqm" not in s
    assert s["is_quote_intent"] is False


async def test_implicit_quote_intent_from_area_plus_business(patch_llm):
    """没说"多少钱",但同时有面积+业态,应推断为报价意图。"""
    patch_llm(FailLLM())
    s = await slots_mod.extract_slots("我开个火锅店 200 平", "storefront")
    assert s["is_quote_intent"] is True


async def test_unit_variants(patch_llm):
    """80㎡ / 80 m² / 80个平米 都应抽到 80。"""
    patch_llm(FailLLM())
    for msg in ("店面 80㎡", "约 80 m²", "大概 80个平米"):
        s = await slots_mod.extract_slots(msg, "storefront")
        assert s["area_sqm"] == 80.0, f"failed on {msg!r}"


async def test_llm_overrides_heuristic_when_both_present(patch_llm):
    """LLM 抽到 area=250,正则也命中 200,LLM 优先。"""
    patch_llm(StubLLM('{"is_quote_intent": true, "area_sqm": 250, "business_type": "饭店"}'))
    s = await slots_mod.extract_slots("我开个饭店 200 平米", "storefront")
    assert s["area_sqm"] == 250.0  # LLM 优先
    assert s["business_type"] == "饭店"
