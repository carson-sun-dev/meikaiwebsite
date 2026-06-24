"""报价工具 — estimate_storefront / office / residential 三大业务线统一入口。

DESIGN 锚点(必读):
- §7.3 第 7 条:展示价 = 历史 ¥/㎡ × `QUOTE_DISPLAY_FACTOR`(默认 0.9 营销折扣)
- §7.3 第 8 条:必须按"空间×工艺"拆分,**禁止单一大数字**;末尾附**固定**免责声明
- §3 Sprint 2:输出"基础/中端/高端"三档 ¥/㎡ 区间
- §15.1 缺陷复盘:Guardrail 输出侧用 quote_stats_per_sqm.json 的 P10-P90 校验

WHY 三档而非单值:
- 装修预算下端到上端可差 6x(基础眼镜店 ¥156/㎡ vs 顶端火锅店 ¥2393/㎡)
- 单值会让用户觉得"被定档了",三档给用户选项 → 提升留资意愿
- 档位映射 P10-P25 / P25-P75 / P75-P90,中端跨距大覆盖典型项目,两端窄反映稀有

WHY 总价不直接给数,而是 low/high 范围:
- ¥/㎡ × 面积 是点估计,但实际项目 ±15% 浮动很正常
- 给范围允许销售在接洽时灵活定价,避免"被锁定"

WHY DISCLAIMER 是模块常量且不可改写:
- 这是合规承诺(对店主、对用户)的固定话术
- 任何调用方都不应该绕过免责声明
"""
from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict

from app.config import get_settings

log = logging.getLogger("tools.quote")

BusinessLine = Literal["residential", "office", "storefront"]
Tier = Literal["basic", "mid", "premium"]

# WHY 固定免责声明(DESIGN §7.3 第 8 条):每条报价末尾必须附此原文,严格不可改写
DISCLAIMER = "这只是AI输出的价格,仅供参考,请联系我们的客户人员,我们将会产出一份更加专业的报价,供您参考。"

# WHY 档位 → 分位区间映射:P10-P25 基础 / P25-P75 中端 / P75-P90 高端
#     P50 故意不单列,因为中位数附近落点最多,中端区间覆盖 P25-P75 自然包含 P50
TIER_QUANTILES: dict[Tier, tuple[str, str]] = {
    "basic":   ("P10", "P25"),
    "mid":     ("P25", "P75"),
    "premium": ("P75", "P90"),
}

# 默认数据路径(相对于项目根)
DEFAULT_STATS_PATH = Path("data/quote_stats_per_sqm.json")
DEFAULT_RATIOS_PATH = Path("data/space_ratios.json")

# WHY 业态典型 ¥/㎡ 兜底(DESIGN §15 Layer 4):
# Sprint 1 收尾时 office n=2 / residential n=1 → 历史数据不足以撑起三档区间(quantiles 在仅
# 1-2 点上插值会塌缩到接近常数)。
# - storefront:基于郑州 2026 行业经验(¥150 眼镜店基础 → ¥2400 火锅店高端,跨度最大)
# - office / residential:2026-06-09 店主基于真实成交经验直接给出锚定值
#     office:×0.9 后显示价控制在 ¥700-900(店主口径);P75-P90 段会塌缩到 ¥900,可接受
#     residential:上限收到历史 ¥1400(显示 ¥1260),下限沿用 ¥500;原 ¥500-2500 跨度过宽被否
# 用 data_quality.stats_source='industry_default' 标记,Guardrail 看到该 source 会放宽阈值
INDUSTRY_DEFAULT_QUANTILES: dict[BusinessLine, dict[str, float]] = {
    "storefront": {"P10": 600.0, "P25": 1000.0, "P50": 1500.0, "P75": 2200.0, "P90": 3000.0},
    "office":     {"P10": 778.0, "P25": 834.0,  "P50": 889.0,  "P75": 945.0,  "P90": 1000.0},
    "residential":{"P10": 500.0, "P25": 650.0,  "P50": 800.0,  "P75": 1100.0, "P90": 1400.0},
}

# WHY 视为"区间塌缩"的阈值:P90 < 1.3 × P10 时三档差小于 30%,用户视角等于"一档",
# 此时 fallback industry default 反而比真数据更有引导性(承认 sample 不足比硬装作有数据好)
COLLAPSED_RATIO = 1.3
MIN_BUCKET_COUNT = 4


class TierQuote(TypedDict):
    per_sqm_low: int
    per_sqm_high: int
    total_low: int
    total_high: int
    breakdown: list[dict]


class QuoteResult(TypedDict):
    business_line: BusinessLine
    business_type: str | None
    area_sqm: float
    tiers: dict[Tier, TierQuote]
    data_quality: dict
    disclaimer: str


@lru_cache(maxsize=1)
def _load_stats(path: str = str(DEFAULT_STATS_PATH)) -> dict:
    """加载 quote_stats_per_sqm.json — 进程内 lru_cache 永久缓存。

    WHY lru_cache 而非全局变量:测试场景可用 _load_stats.cache_clear() 重置;
        生产无重启不变,等价于全局常量。
    """
    p = Path(path)
    if not p.exists():
        log.warning("quote_stats_per_sqm.json 不存在 (%s),报价工具将无统计兜底", p)
        return {"by_business_line": {}, "by_business_type": {}}
    return json.loads(p.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _load_ratios(path: str = str(DEFAULT_RATIOS_PATH)) -> dict:
    p = Path(path)
    if not p.exists():
        log.warning("space_ratios.json 不存在 (%s),报价工具将无空间分项", p)
        return {"by_business_line": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def _round_yuan(v: float) -> int:
    """金额取整到最接近 ¥100 — DESIGN §7.3 心理学:整数比小数友好。"""
    return int(round(v / 100.0) * 100)


def _is_collapsed(b: dict) -> bool:
    """桶质量判定:count 不足或 P10-P90 跨度过小都视为塌缩。"""
    if not b:
        return True
    if b.get("count", 0) < MIN_BUCKET_COUNT:
        return True
    p10, p90 = b.get("P10"), b.get("P90")
    if p10 is None or p90 is None or p10 <= 0:
        return True
    return (p90 / p10) < COLLAPSED_RATIO


def _bucket_for(business_line: BusinessLine, business_type: str | None) -> tuple[dict, str]:
    """三层 fallback:type(精确)→ line(粗类)→ industry_default(经验兜底)。"""
    stats = _load_stats()
    by_type = stats.get("by_business_type", {})
    by_line = stats.get("by_business_line", {})

    # Layer 1:type 桶,需 n>=4 且 P 区间未塌缩
    if business_type:
        key = f"{business_line}/{business_type}"
        cand = by_type.get(key, {})
        if not _is_collapsed(cand):
            return cand, f"by_type:{key}"

    # Layer 2:line 桶
    cand = by_line.get(business_line, {})
    if not _is_collapsed(cand):
        return cand, f"by_line:{business_line}"

    # Layer 3:DESIGN §15 industry_default — 当真数据撑不起三档时,用行业经验值
    log.info("bucket for %s/%s 塌缩或无,fallback industry_default", business_line, business_type)
    return INDUSTRY_DEFAULT_QUANTILES[business_line], f"industry_default:{business_line}"


def _compute_tier(
    bucket: dict,
    area_sqm: float,
    tier: Tier,
    display_factor: float,
    space_ratios: dict[str, float],
) -> TierQuote:
    lo_q, hi_q = TIER_QUANTILES[tier]
    base_lo = bucket.get(lo_q)
    base_hi = bucket.get(hi_q)

    # WHY 空桶 fallback 业态典型值(防 None × None):
    # DESIGN §15 Layer 4 industry default;静默返回 0 给上层会让 LLM 拼出空报价
    if base_lo is None or base_hi is None:
        fallback = {"basic": (600, 1000), "mid": (1000, 1800), "premium": (1800, 2500)}[tier]
        base_lo, base_hi = fallback

    per_lo = base_lo * display_factor
    per_hi = base_hi * display_factor
    total_lo = per_lo * area_sqm
    total_hi = per_hi * area_sqm

    # 分项:每个空间下 low/high 同比例
    breakdown: list[dict] = []
    for space, frac in space_ratios.items():
        breakdown.append({
            "space": space,
            "share_pct": round(frac * 100, 1),
            "amount_low": _round_yuan(total_lo * frac),
            "amount_high": _round_yuan(total_hi * frac),
        })
    # WHY 按金额降序:用户视觉先看到大头,符合"先看重点"心智
    breakdown.sort(key=lambda x: x["amount_high"], reverse=True)

    return TierQuote(
        per_sqm_low=_round_yuan(per_lo),
        per_sqm_high=_round_yuan(per_hi),
        total_low=_round_yuan(total_lo),
        total_high=_round_yuan(total_hi),
        breakdown=breakdown,
    )


def _estimate(
    business_line: BusinessLine,
    area_sqm: float,
    business_type: str | None = None,
) -> QuoteResult:
    """三业务线共用引擎:面积 + 业态细分 → 三档报价 + 分项。"""
    if area_sqm <= 0:
        raise ValueError(f"area_sqm 必须 > 0,得到 {area_sqm}")

    settings = get_settings()
    display_factor = settings.quote_display_factor

    bucket, src = _bucket_for(business_line, business_type)
    ratios_all = _load_ratios().get("by_business_line", {}).get(business_line, {})

    tiers: dict[Tier, TierQuote] = {}
    for tier in ("basic", "mid", "premium"):
        tiers[tier] = _compute_tier(bucket, area_sqm, tier, display_factor, ratios_all)

    return QuoteResult(
        business_line=business_line,
        business_type=business_type,
        area_sqm=area_sqm,
        tiers=tiers,
        data_quality={
            "stats_source": src,
            "sample_count": bucket.get("count", 0),
            "display_factor_applied": display_factor,
            "space_count": len(ratios_all),
        },
        disclaimer=DISCLAIMER,
    )


# WHY 三个公开函数而非单 _estimate(business_line=...):LangGraph / LLM tool calling 协议
#     更喜欢"功能定向"的工具签名,Sprint 2 step 3 把这三个注册为 LangChain tools 时
#     business_line 就内嵌在 tool name 里,LLM 选择哪个工具 == 业态分流第二把锁
def estimate_storefront_quote(area_sqm: float, business_type: str | None = None) -> QuoteResult:
    """门面房店铺装修报价(餐饮/零售/服务业)。area_sqm 必填,业态细分可选(如'火锅店')。"""
    return _estimate("storefront", area_sqm, business_type)


def estimate_office_quote(area_sqm: float, business_type: str | None = None) -> QuoteResult:
    """办公空间装修报价(写字楼/商务楼/学校办公)。area_sqm 必填。"""
    return _estimate("office", area_sqm, business_type)


def estimate_residential_quote(area_sqm: float, business_type: str | None = None) -> QuoteResult:
    """住宅家装报价(自住房/新房/翻新)。area_sqm 必填。"""
    return _estimate("residential", area_sqm, business_type)


def format_quote_for_chat(q: QuoteResult, tier: Tier | None = None, top_n: int = 5) -> str:
    """把 QuoteResult 格式化成对话回复文本。

    WHY 加 tier 参数 + top_n 精简(2026-06-23 用户反馈):
    - 原版一口气列三档 + 10+ 空间分项,用户没问就被信息淹没
    - 加 tier 后:只展示用户选中档的区间 + top_n 分项,文本短 70%
    - 兼容旧调用:tier=None 时退化为三档全展示(保持向后兼容,但 prompt 已不再用)

    WHY 单独抽函数而非让 LLM 自由组织格式:
    - LLM 自由组织容易漏免责声明、加浮夸话术
    - 固定模板保证合规,把 LLM 工作降级为"在模板外做导购话术"
    """
    bl_map = {"storefront": "门面房", "office": "办公空间", "residential": "住宅家装"}
    bt = f"/{q['business_type']}" if q["business_type"] else ""
    tier_zh = {"basic": "基础档", "mid": "中端档", "premium": "高端档"}

    lines = [
        f"📋 美恺装饰 · 参考报价 / {bl_map[q['business_line']]}{bt} / {q['area_sqm']:g}㎡",
        "",
    ]

    if tier is None:
        # 老调用:三档全展示 + mid 分项
        for t_key in ("basic", "mid", "premium"):
            t = q["tiers"][t_key]
            lines.append(
                f"🏷️ {tier_zh[t_key]}  ¥{t['per_sqm_low']:,}-¥{t['per_sqm_high']:,}/㎡  "
                f"总价 ¥{t['total_low']:,}-¥{t['total_high']:,}"
            )
        breakdown = q["tiers"]["mid"]["breakdown"]
        breakdown_label = "💡 中端档分项参考"
    else:
        # 新调用:只出选中档
        t = q["tiers"][tier]
        lines.append(
            f"🏷️ {tier_zh[tier]}  ¥{t['per_sqm_low']:,}-¥{t['per_sqm_high']:,}/㎡"
        )
        lines.append(f"   总价 ¥{t['total_low']:,}-¥{t['total_high']:,}")
        breakdown = t["breakdown"]
        breakdown_label = f"💡 {tier_zh[tier]}主要分项(占比 Top {top_n})"

    # 分项裁剪:按 share_pct 降序取 top_n(默认 5),避免列 10+ 项把用户淹没
    top_items = sorted(breakdown, key=lambda x: x.get("share_pct", 0), reverse=True)[:top_n]
    lines.append("")
    lines.append(f"{breakdown_label}(空间 / 占比):")
    for item in top_items:
        lines.append(
            f"  · {item['space']:6s} {item['share_pct']:5.1f}%   "
            f"¥{item['amount_low']:,}-¥{item['amount_high']:,}"
        )

    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)
