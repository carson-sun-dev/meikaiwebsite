"""报价输出 Guardrail — 在 L2 文本送达用户前做合规校验,违规则交由调用方覆盖/追加权威版本。

DESIGN §5.7.7:输出侧校验,核心防三类异常:
1. 数字不一致 — L2 改动了 quote 工具数字(¥800 写成 ¥1500),或凭空编造新金额
2. 闲聊带价  — 非报价分支的回复不应该出现 ¥ 金额(避免 LLM 闲聊时报数字)
3. 免责声明缺失 — DISCLAIMER 全文必须出现(合规承诺)

WHY 输出侧而非纯靠 prompt:
- Sprint 2 step 3 prompt 已声明"必须原样引用 quote_block",但 LLM 不严格保证
- 输出侧"硬"保证:违规时调用方可覆盖/追加合规模板,合规风险不暴露给用户

WHY 单层(基于 quote 工具输出反查)而非 + P10/P90 范围:
- step 3 之后 LLM 报价路径必经 quote 工具,工具产出即"事实集合",⊆ 检查最精确
- P10/P90 范围是 quote 工具自身的兜底(quote.py 已用),Guardrail 再加一层重复防御边际收益低
- 待 Sprint 2 step 5 RAG 引入"自由组合数据"后再加范围层
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.tools.quote import DISCLAIMER, QuoteResult, format_quote_for_chat


@dataclass
class GuardrailResult:
    ok: bool
    """通过则 True;任何一条规则违反即 False"""

    authoritative_text: str
    """违规时调用方应改用此文本(报价分支 = format_quote_for_chat(quote);其他场景 = 空串)"""

    violations: list[str] = field(default_factory=list)
    """触发的规则名,空表示通过;格式 'rule_name' 或 'rule_name:detail'"""


# WHY 锚定 ¥ 或 元 才视为金额:避免 "200㎡"、"52.8%"、"3 室" 这类被误判为金额
#     LLM 用"万"表达(如"约 1 万元")会漏检 1 < 100 阈值,但"没编新数字"本身合规,接受漏检
_AMOUNT_RE = re.compile(r"(?:¥\s*([\d,]+)|([\d,]+)\s*元)")

# WHY 100 阈值:quote 工具最低产物是 ¥400/㎡(住宅 basic_low);< 100 几乎不可能是合法金额
_AMOUNT_MIN = 100


def _extract_amounts(text: str) -> set[int]:
    """从文本中抠出所有带 ¥ 或 元 标记、且 ≥100 的整数金额。"""
    out: set[int] = set()
    for m in _AMOUNT_RE.finditer(text):
        digits = (m.group(1) or m.group(2) or "").replace(",", "")
        if not digits.isdigit():
            continue
        n = int(digits)
        if n >= _AMOUNT_MIN:
            out.add(n)
    return out


def _collect_quote_amounts(q: QuoteResult | dict[str, Any]) -> set[int]:
    """汇总 quote 工具产出的所有合法金额(per_sqm × {low,high} + total × {low,high} + breakdown)。"""
    amounts: set[int] = set()
    tiers = q.get("tiers", {})
    for tier in ("basic", "mid", "premium"):
        t = tiers.get(tier) or {}
        for k in ("per_sqm_low", "per_sqm_high", "total_low", "total_high"):
            v = t.get(k)
            if isinstance(v, int):
                amounts.add(v)
        for item in t.get("breakdown", []) or []:
            for k in ("amount_low", "amount_high"):
                v = item.get(k)
                if isinstance(v, int):
                    amounts.add(v)
    return amounts


def validate(text: str, quote: dict[str, Any] | None) -> GuardrailResult:
    """对 L2 最终文本做合规校验。

    quote=None  → 非报价分支:任何 ¥/元 金额都视为违规(闲聊不应出价)
    quote=dict  → 报价分支:实际金额必须 ⊆ quote 允许集合,且 DISCLAIMER 必须出现
    """
    violations: list[str] = []

    if quote is None:
        if _extract_amounts(text):
            violations.append("non_quote_branch_has_amount")
        return GuardrailResult(
            ok=not violations,
            authoritative_text="",
            violations=violations,
        )

    allowed = _collect_quote_amounts(quote)
    actual = _extract_amounts(text)
    # WHY 子集而非相等:导购话术可不复读所有数字,但不能引入新数字
    extra = sorted(actual - allowed)
    if extra:
        violations.append(f"unknown_amounts:{extra}")

    if DISCLAIMER not in text:
        violations.append("disclaimer_missing")

    if not violations:
        return GuardrailResult(ok=True, authoritative_text=text, violations=[])

    # 违规 → authoritative 用合规模板;调用方决定覆盖还是追加
    return GuardrailResult(
        ok=False,
        authoritative_text=format_quote_for_chat(quote),  # type: ignore[arg-type]
        violations=violations,
    )
