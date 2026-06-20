"""评测打分逻辑 — Sprint 3 骨架。

WHY 5 个维度各 0.2 分(简单加权 → 0-1 总分):
- 让每条 case 有"细分"的失败原因(business_line 错 vs Guardrail 没触发 vs 关键词漏)
- 加权相同避免主观偏置;V2 接 LLM-as-judge 后再调权重(导购话术质量应该占大头)
- 0-1 总分映射"通过率":通过率 = sum(score) / N,定一个阈值(如 0.85)作为 CI 红线

WHY 评分用 final_text 而非 SSE delta:
- final_text 是 SubGraph 节点 return 的 state 字段,含 Guardrail 修正后的最终文本
- ainvoke 跑完直接拿,无需重组 SSE 流(SSE 是给前端的协议层,评测不该 care)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TurnExpectation:
    user_msg: str
    expected_business_line: str | None = None
    expected_branch: str | None = None  # "quote" / "chat"
    must_contain: list[str] = field(default_factory=list)
    must_not_contain: list[str] = field(default_factory=list)


@dataclass
class TurnObservation:
    """一轮跑完后从 graph state + final_text 收集到的观测值。"""
    final_text: str
    business_line: str | None = None
    branch: str | None = None             # "quote" / "chat" — 由 runner 从 state.quote 推断
    guardrail_ok: bool | None = None      # 由 runner 从 GuardrailResult 收集


@dataclass
class TurnScore:
    """每轮 0-1 分,内含 5 个 0.2 维度分以便诊断。"""
    business_line_score: float = 0.0      # 业态分类正确 → 0.2
    branch_score: float = 0.0             # 分支(quote/chat)判定正确 → 0.2
    must_contain_score: float = 0.0       # 关键词命中率 × 0.2
    must_not_contain_score: float = 0.0   # 禁词全无 → 0.2(出现一个 → 0)
    guardrail_score: float = 0.0          # Guardrail.ok == 期望 → 0.2

    failures: list[str] = field(default_factory=list)

    @property
    def total(self) -> float:
        return (
            self.business_line_score
            + self.branch_score
            + self.must_contain_score
            + self.must_not_contain_score
            + self.guardrail_score
        )


@dataclass
class CaseScore:
    """整个 case(可能多轮)的聚合分数。"""
    name: str
    tags: list[str]
    turn_scores: list[TurnScore]

    @property
    def average(self) -> float:
        if not self.turn_scores:
            return 0.0
        return sum(ts.total for ts in self.turn_scores) / len(self.turn_scores)

    @property
    def all_failures(self) -> list[str]:
        return [f"turn{i+1}: {f}" for i, ts in enumerate(self.turn_scores) for f in ts.failures]


def score_turn(exp: TurnExpectation, obs: TurnObservation) -> TurnScore:
    """单轮评分 — 5 个维度独立打分,失败原因落 failures 字段便于诊断。

    WHY 每维度独立 0/0.2 而非二值通过:
    - must_contain 用命中率(N/M × 0.2)而非 all-or-nothing,差一个关键词不应让整条 0 分
    - 其他 4 维都是布尔判定,但区分 5 个维度让 CI 报告能精确指向"哪类问题"
    """
    s = TurnScore()

    # 1. business_line
    if exp.expected_business_line is None or obs.business_line == exp.expected_business_line:
        s.business_line_score = 0.2
    else:
        s.failures.append(
            f"business_line: expected={exp.expected_business_line!r} got={obs.business_line!r}"
        )

    # 2. branch (quote / chat)
    if exp.expected_branch is None or obs.branch == exp.expected_branch:
        s.branch_score = 0.2
    else:
        s.failures.append(
            f"branch: expected={exp.expected_branch!r} got={obs.branch!r}"
        )

    # 3. must_contain — 命中率打分
    if not exp.must_contain:
        s.must_contain_score = 0.2  # 没要求即视为满分
    else:
        hits = [kw for kw in exp.must_contain if kw in obs.final_text]
        misses = [kw for kw in exp.must_contain if kw not in obs.final_text]
        s.must_contain_score = 0.2 * len(hits) / len(exp.must_contain)
        if misses:
            s.failures.append(f"must_contain misses: {misses}")

    # 4. must_not_contain — 出现一个则归零(零容忍)
    bad_hits = [kw for kw in exp.must_not_contain if kw in obs.final_text]
    if not bad_hits:
        s.must_not_contain_score = 0.2
    else:
        s.failures.append(f"must_not_contain leaked: {bad_hits}")

    # 5. guardrail_ok
    # WHY 期望策略:quote 分支 mock 模式下 Guardrail 必触发(L2 没原样输出 quote_block),
    #     所以 guardrail_ok 应该是 False;但 final_text 含修正段满足 must_contain — 这是
    #     "Guardrail 工作正确"。这里不验 guardrail_ok 的具体值,只验"有值"(说明节点跑完了)
    if obs.guardrail_ok is not None:
        s.guardrail_score = 0.2
    else:
        s.failures.append("guardrail_ok missing(SubGraph 未跑完或观测漏收集)")

    return s


def score_case(
    name: str,
    tags: list[str],
    turn_pairs: list[tuple[TurnExpectation, TurnObservation]],
) -> CaseScore:
    """整 case 评分 — 多轮场景聚合。"""
    turn_scores = [score_turn(exp, obs) for exp, obs in turn_pairs]
    return CaseScore(name=name, tags=tags, turn_scores=turn_scores)


def summarize(scores: list[CaseScore]) -> dict[str, Any]:
    """汇总统计 — 用于 CLI 出表 + JSON 报告 + CI 阈值判定。"""
    if not scores:
        return {"total_cases": 0, "pass_rate": 0.0, "avg_score": 0.0, "failures": []}

    total = sum(s.average for s in scores)
    passing = [s for s in scores if s.average >= 0.8]  # 单条 case 0.8+ 视为通过
    return {
        "total_cases": len(scores),
        "passing_cases": len(passing),
        "pass_rate": len(passing) / len(scores),
        "avg_score": total / len(scores),
        "failures": [
            {"name": s.name, "score": s.average, "issues": s.all_failures}
            for s in scores
            if s.average < 0.8
        ],
    }
