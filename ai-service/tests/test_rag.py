"""tools.rag 单测 — 覆盖空 query / 异常降级 / business_line 过滤 / 标题行剔除。

WHY 全用 monkeypatch 替换 hybrid_search:
- 真 Qdrant 需要 docker compose 起容器,单测应零外部依赖
- hybrid_search 的契约稳定(返回 list[{"score","payload"}]),mock 返回值已足够覆盖业务逻辑
"""
from __future__ import annotations

import pytest

from app.tools import rag as rag_mod
from app.tools.rag import (
    format_examples_for_prompt,
    retrieve_quote_examples,
)


@pytest.fixture(autouse=True)
def reset_label_cache():
    """每个测试前清 _load_project_to_business_line 的 lru_cache,防止跨测污染。"""
    rag_mod._load_project_to_business_line.cache_clear()
    yield
    rag_mod._load_project_to_business_line.cache_clear()


async def test_empty_query_returns_empty(monkeypatch):
    """空消息直接返回 [],不调 hybrid_search。"""
    called = {"n": 0}

    async def _fake_search(**_kw):
        called["n"] += 1
        return []

    monkeypatch.setattr(rag_mod, "hybrid_search", _fake_search)
    out = await retrieve_quote_examples("", "storefront", "火锅店")
    assert out == []
    assert called["n"] == 0


async def test_hybrid_search_exception_degrades_to_empty(monkeypatch):
    """Qdrant 不可达 → 静默返回 [],不抛"""

    async def _boom(**_kw):
        raise ConnectionError("qdrant unreachable")

    monkeypatch.setattr(rag_mod, "hybrid_search", _boom)
    out = await retrieve_quote_examples("我开火锅店 200 平", "storefront", "火锅店")
    assert out == []


async def test_business_line_filter_drops_mismatched(monkeypatch):
    """命中 4 条 hit,其中 2 条 project_id 映射到 office → 应被过滤掉。"""

    async def _fake_search(**_kw):
        return [
            {"score": 0.9, "payload": {"item_name": "门头招牌制作", "subtotal": 38000,
                                       "project_id": "proj_火锅A"}},
            {"score": 0.8, "payload": {"item_name": "工位隔断", "subtotal": 12000,
                                       "project_id": "proj_办公B"}},
            {"score": 0.7, "payload": {"item_name": "厨房排烟", "subtotal": 25000,
                                       "project_id": "proj_火锅A"}},
            {"score": 0.6, "payload": {"item_name": "会议室天花", "subtotal": 9000,
                                       "project_id": "proj_办公B"}},
        ]

    monkeypatch.setattr(rag_mod, "hybrid_search", _fake_search)
    monkeypatch.setattr(
        rag_mod, "_load_project_to_business_line",
        lambda *a, **kw: {"proj_火锅A": "storefront", "proj_办公B": "office"},
    )

    out = await retrieve_quote_examples(
        "我开火锅店 200 平", "storefront", "火锅店", top_k=3,
    )
    assert len(out) == 2  # 两条 storefront,office 被过滤
    assert all(e["business_line"] == "storefront" for e in out)
    assert out[0]["item_name"] == "门头招牌制作"


async def test_group_headers_are_skipped(monkeypatch):
    """无 subtotal & unit_price 的标题行应被丢弃,不占 top_k 名额。"""

    async def _fake_search(**_kw):
        return [
            # 标题行(parse_quotes 漏过的)
            {"score": 0.99, "payload": {"item_name": "大厅装修", "subtotal": None,
                                        "unit_price": None, "project_id": "proj_A"}},
            {"score": 0.9, "payload": {"item_name": "石膏板吊顶", "subtotal": 5800,
                                       "project_id": "proj_A"}},
            {"score": 0.8, "payload": {"item_name": "墙面乳胶漆", "unit_price": 35,
                                       "subtotal": None, "project_id": "proj_A"}},
        ]

    monkeypatch.setattr(rag_mod, "hybrid_search", _fake_search)
    monkeypatch.setattr(
        rag_mod, "_load_project_to_business_line",
        lambda *a, **kw: {"proj_A": "storefront"},
    )

    out = await retrieve_quote_examples("装修预算", "storefront", None, top_k=5)
    # 标题行被丢,真 line item(石膏板 + 乳胶漆)保留
    names = [e["item_name"] for e in out]
    assert "大厅装修" not in names
    assert "石膏板吊顶" in names
    assert "墙面乳胶漆" in names


async def test_top_k_cap(monkeypatch):
    """召回 10 条,top_k=2 → 最多返回 2 条。"""

    async def _fake_search(**_kw):
        return [
            {"score": 1.0 - i * 0.1,
             "payload": {"item_name": f"项目{i}", "subtotal": 1000 * i,
                         "project_id": f"proj_{i}"}}
            for i in range(1, 11)
        ]

    monkeypatch.setattr(rag_mod, "hybrid_search", _fake_search)
    monkeypatch.setattr(
        rag_mod, "_load_project_to_business_line",
        lambda *a, **kw: {f"proj_{i}": "storefront" for i in range(1, 11)},
    )

    out = await retrieve_quote_examples("装修", "storefront", None, top_k=2)
    assert len(out) == 2
    assert out[0]["item_name"] == "项目1"
    assert out[1]["item_name"] == "项目2"


async def test_missing_label_mapping_does_not_filter(monkeypatch):
    """projects_labeled.jsonl 缺失或映射不全时,放过未知 project_id 的 item(不一棒打死)。"""

    async def _fake_search(**_kw):
        return [
            {"score": 0.9, "payload": {"item_name": "踢脚线", "subtotal": 600,
                                       "project_id": "proj_未知"}},
        ]

    monkeypatch.setattr(rag_mod, "hybrid_search", _fake_search)
    monkeypatch.setattr(rag_mod, "_load_project_to_business_line", lambda *a, **kw: {})

    out = await retrieve_quote_examples("家里 100 平", "residential", None)
    assert len(out) == 1
    assert out[0]["item_name"] == "踢脚线"


def test_format_examples_for_prompt_empty():
    assert format_examples_for_prompt([]) == ""


def test_format_examples_for_prompt_truncates_long_spec():
    long_spec = "工艺说明" * 50  # 200 字
    examples = [
        rag_mod.QuoteExample(item_name="门头招牌", spec=long_spec, subtotal=38000,
                             unit_price=None, project_id="x", business_line="storefront",
                             score=0.9),
    ]
    out = format_examples_for_prompt(examples)
    assert "门头招牌" in out
    # 整段被截到 60 字
    line = [ln for ln in out.split("\n") if "门头招牌" in ln][0]
    # 1. + 空格 + 内容 → 内容截到 ≤60 字
    content = line.split("1.", 1)[1].strip()
    assert len(content) <= 60


def test_format_examples_does_not_leak_money():
    """格式化函数不应把金额暴露在 prompt 段里(Guardrail 不允许新数字出现)。"""
    examples = [
        rag_mod.QuoteExample(item_name="厨房排烟", spec="304 不锈钢风管", subtotal=25000,
                             unit_price=180, project_id="x", business_line="storefront",
                             score=0.9),
    ]
    out = format_examples_for_prompt(examples)
    assert "25000" not in out
    assert "180" not in out
    assert "厨房排烟" in out
