"""quote_sanity.validate 单元测试 — 报价/闲聊两种 quote 状态 × 三类违规。

WHY 不 mock LLM:validate 是纯函数,quote 走真 estimate_*_quote 拿结构化输入即可,
    这样测试也兼带验证 _collect_quote_amounts 在真实 quote 字典结构上的索引正确性。
"""
from __future__ import annotations

import pytest

from app.guardrails.quote_sanity import (
    _collect_quote_amounts,
    _extract_amounts,
    validate,
)
from app.tools.quote import DISCLAIMER, estimate_storefront_quote, format_quote_for_chat


@pytest.fixture
def sample_quote():
    return estimate_storefront_quote(120, "饭店")


# ---- 报价分支:合规 / 数字越界 / 免责缺失 ----

def test_compliant_quote_text_passes(sample_quote):
    text = format_quote_for_chat(sample_quote)
    r = validate(text, sample_quote)
    assert r.ok is True
    assert r.violations == []
    assert r.authoritative_text == text


def test_extra_amount_blocks_and_provides_authoritative(sample_quote):
    """L2 编了一个不在 quote 集合里的 ¥99999 → 必须挡下并给权威版本。"""
    text = format_quote_for_chat(sample_quote) + "\n特价优惠:¥99999/㎡ 仅限本周!"
    r = validate(text, sample_quote)
    assert r.ok is False
    assert any("99999" in v for v in r.violations), r.violations
    assert r.authoritative_text == format_quote_for_chat(sample_quote)


def test_disclaimer_missing_blocks(sample_quote):
    text = format_quote_for_chat(sample_quote).replace(DISCLAIMER, "")
    r = validate(text, sample_quote)
    assert r.ok is False
    assert "disclaimer_missing" in r.violations


def test_disclaimer_partial_does_not_count(sample_quote):
    """只贴一半 DISCLAIMER 也算缺失 — 必须全文出现。"""
    half = DISCLAIMER[: len(DISCLAIMER) // 2]
    text = format_quote_for_chat(sample_quote).replace(DISCLAIMER, half)
    r = validate(text, sample_quote)
    assert r.ok is False
    assert "disclaimer_missing" in r.violations


# ---- 非报价分支:闲聊不应带价 ----

def test_non_quote_branch_no_amount_ok():
    r = validate("您好,请问您想装修什么类型的空间?", quote=None)
    assert r.ok is True
    assert r.violations == []
    assert r.authoritative_text == ""


def test_non_quote_branch_with_amount_blocks():
    r = validate("我们大概 ¥500/㎡ 起步", quote=None)
    assert r.ok is False
    assert "non_quote_branch_has_amount" in r.violations


# ---- 金额抽取器边界:避免误报百分比/面积/室数 ----

def test_percentage_and_area_not_amount(sample_quote):
    """100㎡ / 52.8% / 3 室 都不带 ¥ 或 元,不应当作金额触发违规。"""
    extra = "\n我们做过 100㎡ 案例,使用率 52.8%,共 3 室,排烟通过 4 米管道布置。"
    text = format_quote_for_chat(sample_quote) + extra
    r = validate(text, sample_quote)
    assert r.ok is True, r.violations


def test_yuan_suffix_is_recognized(sample_quote):
    """"5000元" 写法应被抽到,5000 不在 quote 集合 → 违规。"""
    text = format_quote_for_chat(sample_quote) + "\n另外开荒清洁 5000元。"
    r = validate(text, sample_quote)
    assert r.ok is False
    assert any("5000" in v for v in r.violations), r.violations


def test_thousand_separator_normalized(sample_quote):
    """¥56,000 与 56000 应等价比较,quote 工具产出无千分位,LLM 输出有,不能错杀。"""
    allowed = _collect_quote_amounts(sample_quote)
    big = next(iter(a for a in allowed if a >= 10000))
    text = f"参考报价:¥{big:,}/项目。\n" + DISCLAIMER
    r = validate(text, sample_quote)
    assert r.ok is True, r.violations


def test_small_number_below_threshold_ignored():
    """< 100 的数字(1万元 中的 1,3 室 中的 3)不算金额。"""
    extracted = _extract_amounts("¥50/㎡  3 元  10元  ¥99")
    # 50/3/10/99 都 < 100 → 全部过滤
    assert extracted == set()


def test_extract_amount_with_yuan_and_comma():
    """¥56,000 / 64,000元 都应抽到正确整数。"""
    extracted = _extract_amounts("¥56,000-¥64,000 另需 5,000元")
    assert extracted == {56000, 64000, 5000}
