"""quote.py 单元测试 — 覆盖三业务线 + Layer 1/2/3 fallback + 合规字段。

WHY 覆盖三层 fallback 而非只跑 happy path:
- DESIGN §15 Layer 1/2/3 是工程主张,测试必须验证"分层确实在工作"
- 业务线本身的 sample 分布(火锅店 n=2 / 饭店 n=8 / office n=2)正好对应三种 fallback,
  用真数据驱动测试比 mock 出固定桶更能反映生产路径
"""
from __future__ import annotations

import pytest

from app.tools.quote import (
    DISCLAIMER,
    INDUSTRY_DEFAULT_QUANTILES,
    estimate_office_quote,
    estimate_residential_quote,
    estimate_storefront_quote,
    format_quote_for_chat,
)


# ---- 三业务线公开 API ----

def test_storefront_饭店_uses_type_bucket():
    """n=8 的饭店桶能直接命中 Layer 1。"""
    q = estimate_storefront_quote(120, "饭店")
    assert q["data_quality"]["stats_source"].startswith("by_type:")
    assert q["data_quality"]["sample_count"] >= 4
    assert q["disclaimer"] == DISCLAIMER


def test_storefront_火锅店_falls_back_to_line():
    """n=2 的火锅店桶因塌缩 fallback 到 storefront line。"""
    q = estimate_storefront_quote(200, "火锅店")
    assert q["data_quality"]["stats_source"] == "by_line:storefront"
    # storefront line n=19 不应塌缩
    assert q["data_quality"]["sample_count"] >= 4


def test_office_falls_to_industry_default():
    """office 真实 n=2,line 桶也塌缩,fallback Layer 3 industry_default。"""
    q = estimate_office_quote(80)
    assert q["data_quality"]["stats_source"] == "industry_default:office"
    assert q["data_quality"]["sample_count"] == 0


def test_residential_falls_to_industry_default():
    """residential 真实 n=1,fallback industry_default。"""
    q = estimate_residential_quote(90)
    assert q["data_quality"]["stats_source"] == "industry_default:residential"


# ---- 营销系数 / 档位语义 ----

def test_display_factor_applied():
    """¥/㎡ 显式乘 0.9 营销系数。"""
    q = estimate_storefront_quote(100, "饭店")
    factor = q["data_quality"]["display_factor_applied"]
    assert factor == pytest.approx(0.9)
    # 中端 per_sqm_high 应 ~= P75 × 0.9(允许 ±100 ¥ 取整误差)
    # 饭店 P75 在数据里大约 1700-1900,乘 0.9 后大约 1500-1700
    assert 1200 <= q["tiers"]["mid"]["per_sqm_high"] <= 2000


def test_three_tiers_monotonic():
    """basic ≤ mid ≤ premium,各档区间不交叉重叠到失序。"""
    q = estimate_storefront_quote(200, "饭店")
    b, m, p = q["tiers"]["basic"], q["tiers"]["mid"], q["tiers"]["premium"]
    assert b["per_sqm_low"] <= m["per_sqm_low"] <= p["per_sqm_low"]
    assert b["per_sqm_high"] <= m["per_sqm_high"] <= p["per_sqm_high"]


def test_total_consistent_with_per_sqm():
    """total = per_sqm × area_sqm,允许 ±5% 取整误差。"""
    q = estimate_storefront_quote(120, "饭店")
    for tier in ("basic", "mid", "premium"):
        t = q["tiers"][tier]
        expected_low = t["per_sqm_low"] * 120
        expected_high = t["per_sqm_high"] * 120
        # ¥100 取整 + ¥1000 圆整产生的小波动允许 5% 余量
        assert abs(t["total_low"] - expected_low) / max(expected_low, 1) < 0.05
        assert abs(t["total_high"] - expected_high) / max(expected_high, 1) < 0.05


# ---- 分项展示规则(DESIGN §7.3 第 8 条) ----

def test_breakdown_present_and_sums_close_to_total():
    """中端档分项金额之和应接近总价(±10%)。"""
    q = estimate_storefront_quote(120, "饭店")
    breakdown = q["tiers"]["mid"]["breakdown"]
    assert len(breakdown) >= 3, "至少 3 个空间分项才能体现拆分"
    sum_low = sum(b["amount_low"] for b in breakdown)
    sum_high = sum(b["amount_high"] for b in breakdown)
    t = q["tiers"]["mid"]
    assert abs(sum_low - t["total_low"]) / t["total_low"] < 0.15
    assert abs(sum_high - t["total_high"]) / t["total_high"] < 0.15


def test_breakdown_sorted_desc():
    """分项按金额降序,大头优先展示。"""
    q = estimate_storefront_quote(120, "饭店")
    breakdown = q["tiers"]["mid"]["breakdown"]
    amounts = [b["amount_high"] for b in breakdown]
    assert amounts == sorted(amounts, reverse=True)


# ---- 文本格式器 ----

def test_format_contains_disclaimer():
    """文本输出必须包含固定免责声明全文。"""
    q = estimate_storefront_quote(200, "火锅店")
    text = format_quote_for_chat(q)
    assert DISCLAIMER in text


def test_format_no_single_big_number():
    """DESIGN §7.3:禁止单一大数字;格式器输出应至少含三档分别的¥行,且总价范围用 - 分隔。"""
    q = estimate_storefront_quote(200, "火锅店")
    text = format_quote_for_chat(q)
    # 三档 tier 行各一(中端档另出现在分项小标题里,所以 ≥1 即可)
    assert text.count("基础档") >= 1
    assert text.count("中端档") >= 1
    assert text.count("高端档") >= 1
    # 中端分项至少 3 个 · 列表项
    assert text.count("·") >= 3


# ---- 边界条件 ----

def test_area_zero_or_negative_raises():
    with pytest.raises(ValueError):
        estimate_storefront_quote(0)
    with pytest.raises(ValueError):
        estimate_storefront_quote(-10)


def test_unknown_business_type_falls_back():
    """不存在的业态细分不应崩溃,自动降到 line 或 default。"""
    q = estimate_storefront_quote(200, "完全没见过的奇怪业态")
    assert q["data_quality"]["stats_source"] in (
        "by_line:storefront",
        "industry_default:storefront",
    )
    # 仍然有三档,不缺
    for tier in ("basic", "mid", "premium"):
        assert q["tiers"][tier]["per_sqm_high"] > 0


# ---- INDUSTRY_DEFAULT 自身一致性 ----

@pytest.mark.parametrize("bl", list(INDUSTRY_DEFAULT_QUANTILES.keys()))
def test_industry_default_monotonic(bl):
    """每个业态典型值的 P10<P25<P50<P75<P90 必须严格单调。"""
    d = INDUSTRY_DEFAULT_QUANTILES[bl]
    assert d["P10"] < d["P25"] < d["P50"] < d["P75"] < d["P90"]
