"""空间分项 ETL — 从 2559 条 line item 抽"空间×工艺"成本占比,供 estimate_*_quote 工具做分项展示。

WHY 必须分项展示:
- DESIGN §7.3 第 8 条:报价禁止单一大数字("装修费用 ¥53 万"会吓退用户)
- 心理学:"门头 ¥3 万 + 厨房 ¥12 万 + 大厅 ¥18 万" 比 ¥53 万亲切得多,客户觉得对成本可控
- 用户决定留资的临界点取决于"是否觉得报价可理解",分项展示直接提升留资转化

WHY 此 ETL 必须真从数据来,不能拍脑袋系数:
- 行业经验值在不同业态差异极大(火锅厨房占 30% vs 服装店厨房 0%)
- 拍数据会被店主一眼看穿"不像真实项目";走 23 份历史数据聚合的比例,
  即使数据样本小,反推的比例至少符合美恺这家公司的承接结构,可信度高

抽取策略 — section header carry-forward:
- 报价单的 line item 通常按"大厅装修(header,无金额) → 石膏板吊顶 16.8㎡ ¥2184 → 木隔栅吊顶 ¥7584 → ..."组织
- 单独看 item_name "石膏板吊顶" 没有空间信息,但跟随的 section header "大厅装修" 携带空间归属
- 算法:逐项扫描 → 命中 SPACE_KEYWORDS 则更新 current_space → 后续含 subtotal 的项归 current_space
- 同 sheet 内的 header 衰减规则:遇到新 header 时重置 current_space(不跨 sheet 继承)

WHY 空间归属之外还要单列"水电/空调/家具":
- 装修业内"水电""空调""家具"通常另起 sheet 或大段独立预算,跨房间无法归属
- 在 SPACE_KEYWORDS 里把它们作"工艺/机电类"虚拟空间,与物理房间并列展示;
  这正是 DESIGN §7.3 第 8 条要求的"空间 + 工艺"两种维度同时拆分

用法:
    python -m etl.extract_space_breakdown

输入:data/quotes.jsonl + data/projects_labeled.jsonl
输出:data/space_ratios.json
"""
from __future__ import annotations

import argparse
import json
import logging
import statistics
from collections import defaultdict
from pathlib import Path

log = logging.getLogger("etl.extract_space_breakdown")

# WHY 业态独立的关键词表:storefront / office / residential 的空间命名几乎不重叠
#     (storefront 没有"卧室",residential 没有"包间"),分表能避免误归类。
# WHY 关键词顺序 = 优先级:具体词在前(包间 > 大厅),歧义词最后命中
SPACE_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "storefront": {
        # 物理空间(餐饮典型分区)
        "门头": ["门头", "招牌", "门面", "门廊", "外立面", "前脸", "店招", "logo"],
        "包间": ["包间", "包房", "包厢", "vip"],
        "厨房": ["厨房", "操作间", "明厨", "厨房间", "灶台", "灶具", "厨电", "炊事"],
        "卫生间": ["卫生间", "洗手间", "厕所", "盥洗", "卫浴"],
        "收银吧台": ["收银", "吧台", "前台", "水吧", "茶水台"],
        "大厅": ["大厅", "前厅", "公共区", "用餐区", "营业厅", "营业区", "卡座", "散座", "雅座", "橱窗", "走廊"],
        # 工艺/机电类(横向贯穿,单列)
        "水电": ["水电", "给水", "排水", "电气", "线缆", "插座", "配电", "开关", "强电", "弱电"],
        "空调暖通": ["空调", "新风", "通风", "暖通", "中央空调", "风管"],
        "排烟": ["排烟", "排油烟", "烟道", "油烟"],
        "家具软装": ["家具", "桌椅", "软装", "灯具", "灯光", "窗帘", "卡座沙发", "餐桌"],
    },
    "office": {
        "前台": ["前台", "接待区", "接待台"],
        "工位区": ["工位", "办公桌", "开放办公", "员工区", "办公区"],
        "会议室": ["会议", "会议室", "洽谈室", "培训室"],
        "茶水间": ["茶水", "茶水间", "休息区", "茶歇"],
        "卫生间": ["卫生间", "洗手间", "厕所", "盥洗"],
        "强弱电": ["强电", "弱电", "网络", "综合布线", "配电", "电气", "插座", "线缆"],
        "空调暖通": ["空调", "新风", "通风", "中央空调", "暖通"],
        "家具": ["工位桌椅", "办公桌", "家具", "屏风", "工位家具", "会议桌"],
    },
    "residential": {
        "客厅": ["客厅", "起居室", "客餐厅"],
        "卧室": ["卧室", "主卧", "次卧", "儿童房", "书房", "睡房"],
        "厨房": ["厨房", "橱柜"],
        "卫生间": ["卫生间", "洗手间", "厕所", "淋浴", "卫浴"],
        "阳台": ["阳台", "晾衣", "露台"],
        "水电": ["水电", "给水", "排水", "电气", "线缆", "插座", "配电"],
        "软装": ["软装", "家具", "灯具", "灯光", "窗帘", "床品"],
    },
}


def classify_item(text: str, business_line: str) -> str | None:
    """返回 item_name 命中的空间名,无命中返回 None。"""
    if not text:
        return None
    text_lower = text.lower()
    spaces = SPACE_KEYWORDS.get(business_line, {})
    for space_name, keywords in spaces.items():
        for kw in keywords:
            if kw in text or kw in text_lower:
                return space_name
    return None


def aggregate_project(items: list[dict], business_line: str) -> dict[str, float]:
    """单项目内逐 line item 扫描,section header carry-forward 归属空间。

    返回 {space_name: total_subtotal}。
    """
    by_space: dict[str, float] = defaultdict(float)
    current_space: str | None = None
    current_sheet: str | None = None

    for it in items:
        sheet = it.get("sheet")
        name = it.get("item_name") or ""
        subtotal = it.get("subtotal")

        # WHY 跨 sheet 重置 current_space:
        # 不同 sheet 通常是不同口径(土建 sheet vs 水电 sheet),carry-forward 跨 sheet 会污染
        if sheet != current_sheet:
            current_space = None
            current_sheet = sheet

        # 1) 试图从 item_name 自身分类(精确命中,无关 subtotal 有无)
        hit = classify_item(name, business_line)

        # 2) 也试 raw_row 的"工艺说明"字段(部分预算单细节都堆在备注里)
        if hit is None:
            raw = it.get("raw_row") or {}
            for k, v in raw.items():
                if k and ("说明" in k or "工艺" in k or "材料" in k) and isinstance(v, str):
                    hit = classify_item(v, business_line)
                    if hit:
                        break

        if hit is not None:
            current_space = hit
            # WHY 命中的 row 也参与累计:section header(subtotal=null)自然跳过,
            # 而具体施工项命中 keyword 的(如"明厨排烟管 ¥3500")也归对应空间
            if subtotal is not None and subtotal > 0:
                by_space[hit] += float(subtotal)
        elif current_space is not None and subtotal is not None and subtotal > 0:
            # 无命中,沿用 carry-forward 空间
            by_space[current_space] += float(subtotal)
        # 三都不满足 → 跳过(无空间归属 + 无金额,要么是表头要么是无效行)

    return dict(by_space)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects", default="data/projects_labeled.jsonl")
    ap.add_argument("--items", default="data/quotes.jsonl")
    ap.add_argument("--out", default="data/space_ratios.json")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    # 索引 line items by project
    items_by_project: dict[str, list[dict]] = defaultdict(list)
    for line in Path(args.items).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        it = json.loads(line)
        items_by_project[it["project_id"]].append(it)

    # 业态分桶汇总(每项目算占比,再业态内做几何平均)
    # WHY 算项目内占比再平均,而不是把所有项目金额堆一起算:
    # - 大项目(财经政法大学餐厅 ¥128 万)会把比例分布压成它一家的画像
    # - 项目内归一化后平均,小项目和大项目同权,更能反映"典型项目结构"
    ratios_by_line: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    project_coverage: dict[str, list[float]] = defaultdict(list)

    for line in Path(args.projects).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        p = json.loads(line)
        pid = p["project_id"]
        bl = p.get("business_line")
        if bl not in SPACE_KEYWORDS:
            continue

        items = items_by_project.get(pid, [])
        by_space = aggregate_project(items, bl)
        classified_sum = sum(by_space.values())
        if classified_sum <= 0:
            log.warning("project %s 无任何空间归属,跳过", pid)
            continue

        # WHY 用 classified_sum 而非项目 total_amount 做分母:
        # 项目总价里有大量无法归类的"小计/合计/管理费",拿去做分母会让比例偏低
        # 用已分类的总和做分母,比例直接反映"在能识别的开支里各空间占多少"
        for sp, amt in by_space.items():
            ratios_by_line[bl][sp].append(amt / classified_sum)

        # 覆盖率:项目 total 中被识别的份额(辅助评估 ETL 质量)
        total = p.get("total_amount") or 0
        if total > 0:
            project_coverage[bl].append(classified_sum / float(total))

    # 输出
    out: dict = {
        "schema_version": "1",
        "metric": "fraction_of_classified_spend",
        "note": "每业态下'空间×工艺'各占已分类施工开支的平均比例(项目内归一化后业态内均值)",
        "by_business_line": {},
        "diagnostics": {},
    }

    log.info("=== 空间分项比例 ===")
    for bl in ("storefront", "office", "residential"):
        per_space_avg: dict[str, float] = {}
        sample_size: dict[str, int] = {}
        for sp, vals in ratios_by_line[bl].items():
            if vals:
                per_space_avg[sp] = round(statistics.mean(vals), 4)
                sample_size[sp] = len(vals)
        # WHY 二次归一化:并非每个项目都覆盖到全部空间,均值之后 sum 不一定为 1
        s = sum(per_space_avg.values()) or 1.0
        per_space_norm = {k: round(v / s, 4) for k, v in per_space_avg.items()}
        out["by_business_line"][bl] = per_space_norm

        cov = project_coverage[bl]
        out["diagnostics"][bl] = {
            "project_count": len(cov),
            "avg_classified_coverage": round(statistics.mean(cov), 3) if cov else None,
            "sample_size_per_space": sample_size,
        }

        log.info("[%s] coverage=%s%% n=%d",
                 bl,
                 round(statistics.mean(cov) * 100, 1) if cov else "n/a",
                 len(cov))
        for sp, frac in sorted(per_space_norm.items(), key=lambda x: -x[1]):
            log.info("    %-10s %5.1f%%   (n=%d)", sp, frac * 100, sample_size[sp])

    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s", args.out)


if __name__ == "__main__":
    main()
