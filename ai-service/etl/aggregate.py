"""
业态聚合:按 business_line 分桶,算两套分位数 —— total_amount 与 per_sqm_yuan。

输出两个文件:
- data/quote_stats.json          → 总价分位数(向后兼容旧消费者)
- data/quote_stats_per_sqm.json   → ¥/㎡ 分位数(Sprint 1 收尾新增,供 §5.7.7 Guardrail 输出侧校验)

WHY 两个文件而非一个 nested 结构:
- Guardrail 在 LLM 报价格出来后,只需要拿一份 ¥/㎡ 分位数比较;读两个独立 JSON 比解析嵌套清晰
- 总价分布在面试中作为"项目规模总览"展示,¥/㎡ 才是行业内可比维度,语义不同

WHY 不算平均值:
- 装修预算长尾严重(单个高端项目可拉高均值 50%+)
- 中位数 / 分位数更代表"典型项目",符合 Guardrail 用途

WHY P10/P90 而非 ±2σ:
- ¥/㎡ 不是正态分布(右偏明显:基础档 ¥150 vs 高端 ¥2400)
- 分位数对长尾稳健,σ 会被高端项目拉宽到失去判别力

用法:
    python -m etl.aggregate

输入:data/projects_labeled.jsonl
输出:data/quote_stats.json + data/quote_stats_per_sqm.json
"""
from __future__ import annotations

import argparse
import json
import logging
import statistics
from collections import defaultdict
from pathlib import Path

log = logging.getLogger("etl.aggregate")


def quantiles_safe(values: list[float], n_buckets: int = 10) -> dict[str, float]:
    """返回 P10/P25/P50/P75/P90。<2 条样本时返回单值(无法分位)。"""
    if not values:
        return {}
    if len(values) == 1:
        v = round(values[0], 2)
        return {f"P{p}": v for p in (10, 25, 50, 75, 90)}
    # statistics.quantiles 需要 ≥ 2 个样本,n=10 给十分位
    qs = statistics.quantiles(values, n=n_buckets, method="exclusive")
    # qs[i] = 第 (i+1)*10 百分位,所以 P10=qs[0], P25 需插值
    p10 = qs[0]
    p25 = (qs[1] + qs[2]) / 2  # 近似 P25(20% 与 30% 中点)
    p50 = qs[4]  # 50%
    p75 = (qs[6] + qs[7]) / 2  # 近似 P75
    p90 = qs[8]
    return {
        "P10": round(p10, 2),
        "P25": round(p25, 2),
        "P50": round(p50, 2),
        "P75": round(p75, 2),
        "P90": round(p90, 2),
    }


def summarize_bucket(vals: list[float]) -> dict:
    """单桶汇总:count/min/max/mean + 分位数。"""
    return {
        "count": len(vals),
        "min": round(min(vals), 2),
        "max": round(max(vals), 2),
        "mean": round(statistics.mean(vals), 2),
        **quantiles_safe(vals),
    }


def build_stats(
    projects: list[dict],
    metric_key: str,
    metric_name: str,
    note: str,
    min_type_count: int = 2,
) -> tuple[dict, int]:
    """通用聚合:按 business_line + business_type 两层分桶,产 stats dict + missing 计数。

    WHY 抽出公共函数:total_amount / per_sqm_yuan 两套统计形态相同,只是 metric_key 不同;
        把分桶/统计逻辑参数化避免复制粘贴维护两份。
    """
    by_line: dict[str, list[float]] = defaultdict(list)
    by_type: dict[str, list[float]] = defaultdict(list)
    missing = 0

    for p in projects:
        v = p.get(metric_key)
        if v is None:
            missing += 1
            continue
        bl = p.get("business_line") or "unknown"
        bt = p.get("business_type") or "unknown"
        by_line[bl].append(float(v))
        by_type[f"{bl}/{bt}"].append(float(v))

    out: dict = {
        "schema_version": "2",
        "metric": metric_name,
        "note": note,
        "missing_count": missing,
        "by_business_line": {},
        "by_business_type": {},
    }

    for bl, vals in sorted(by_line.items()):
        out["by_business_line"][bl] = summarize_bucket(vals)

    for bt, vals in sorted(by_type.items()):
        # WHY n>=2 才入细分桶:单样本分位数无意义,Guardrail 用粗 bucket 兜底即可
        if len(vals) < min_type_count:
            continue
        out["by_business_type"][bt] = summarize_bucket(vals)

    return out, missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="data/projects_labeled.jsonl")
    ap.add_argument("--out-total", default="data/quote_stats.json")
    ap.add_argument("--out-per-sqm", default="data/quote_stats_per_sqm.json")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    projects = [
        json.loads(line)
        for line in Path(args.src).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    log.info("loaded %d projects", len(projects))

    # ---- 总价桶(向后兼容) ----
    total_stats, miss_total = build_stats(
        projects,
        metric_key="total_amount",
        metric_name="total_amount_yuan",
        note="项目总价分位数,与 ¥/㎡ 一同作为 Guardrail 输出侧 P10-P90 校验参考",
    )
    log.info("=== 总价 by business_line ===")
    for bl, s in total_stats["by_business_line"].items():
        log.info("  %-12s n=%2d  P25=¥%-12s P50=¥%-12s P75=¥%-12s",
                 bl, s["count"], s.get("P25", "-"), s.get("P50", "-"), s.get("P75", "-"))

    # ---- ¥/㎡ 桶(新增,Sprint 1 收尾核心) ----
    per_sqm_stats, miss_psm = build_stats(
        projects,
        metric_key="per_sqm_yuan",
        metric_name="per_sqm_yuan",
        note="单位面积造价 ¥/㎡ 分位数,Sprint 2 §5.7.7 Guardrail 直接用此区间反查 LLM 报价合理性",
    )
    log.info("")
    log.info("=== ¥/㎡ by business_line ===")
    for bl, s in per_sqm_stats["by_business_line"].items():
        log.info("  %-12s n=%2d  P10=¥%-6s P25=¥%-6s P50=¥%-6s P75=¥%-6s P90=¥%-6s",
                 bl, s["count"],
                 s.get("P10", "-"), s.get("P25", "-"), s.get("P50", "-"),
                 s.get("P75", "-"), s.get("P90", "-"))

    log.info("")
    log.info("=== ¥/㎡ by business_type(n≥2)===")
    for bt, s in per_sqm_stats["by_business_type"].items():
        log.info("  %-30s n=%2d  P50=¥%s", bt, s["count"], s.get("P50", "-"))

    log.info("")
    log.info("missing total_amount: %d / %d", miss_total, len(projects))
    log.info("missing per_sqm_yuan: %d / %d (无 area 项目)", miss_psm, len(projects))

    Path(args.out_total).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_total).write_text(json.dumps(total_stats, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s", args.out_total)
    Path(args.out_per_sqm).write_text(json.dumps(per_sqm_stats, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s", args.out_per_sqm)


if __name__ == "__main__":
    main()
