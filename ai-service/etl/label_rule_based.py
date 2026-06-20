"""
规则法给 23 个项目打业态标签:从文件名 + 前 N 条 line item 名抽关键词推断。

WHY 先做规则法再 LLM 兜底(DESIGN §3 Sprint 1):
- 规则法零成本、可复现、可 diff;~70-80% 项目能高置信度命中(文件名直接含业态词)
- 剩下的 unknown 才给 L0 模型推,省调用费且 LLM 失误概率低
- 输出格式与 etl/label_with_llm.py 兼容,后者用 --only-unknown 仅补漏

业态映射规则(关键词命中 → business_line + business_type):
- storefront(门面房,核心业务):火锅/茶馆/咖啡/奶茶/眼镜/店/宴/餐厅/生煎/饸饹/瓦舍/...
- office(办公/学校):办公室/写字楼/学校/教室/科技园
- residential(住宅):别墅/家装/花园/小区/新房/住宅

用法:
    python -m etl.label_rule_based

输入:data/projects.jsonl + data/quotes.jsonl
输出:data/projects_labeled.jsonl(每行加 business_line / business_type / label_source 字段)
"""
from __future__ import annotations

import argparse
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Literal

log = logging.getLogger("etl.label_rule_based")

BusinessLine = Literal["residential", "office", "storefront", "unknown"]

# WHY 单 dict 而非函数式 if-else 链:规则可见、可 diff、可 unit test
# 顺序 = 优先级:从特异性最高(细分业态)到特异性最低(通用关键字"店")
RULES: list[tuple[str, BusinessLine, str]] = [
    # storefront - 餐饮细分(最具识别度,放最前)
    ("火锅", "storefront", "火锅店"),
    ("茶馆", "storefront", "茶馆"),
    ("茶饮", "storefront", "茶饮店"),
    ("咖啡", "storefront", "咖啡店"),
    ("奶茶", "storefront", "奶茶店"),
    ("生煎", "storefront", "生煎店"),
    ("饸饹", "storefront", "饸饹店"),
    ("瓦舍", "storefront", "火锅店"),  # WHY 瓦舍是 4 川/河南火锅常见品牌后缀,经验判定
    ("宴", "storefront", "餐饮"),
    # storefront - 零售/服务细分
    ("眼镜", "storefront", "眼镜店"),
    ("眼睛", "storefront", "眼镜店"),  # WHY 容忍 typo:文件名"三门峡眼睛店"明显笔误
    ("服装", "storefront", "服装店"),
    ("美容", "storefront", "美容院"),
    ("便利店", "storefront", "便利店"),
    # office - 严格识别(学校算 institutional 归入 office)
    ("办公室", "office", "办公室"),
    ("写字楼", "office", "写字楼"),
    ("商学院", "office", "学校办公"),
    ("学校", "office", "学校"),
    ("教室", "office", "教室"),
    ("科技园", "office", "科技园"),
    # residential - 住宅类
    ("别墅", "residential", "别墅"),
    ("家装", "residential", "住宅"),
    ("花园", "residential", "住宅小区"),
    ("新房", "residential", "住宅"),
    ("住宅", "residential", "住宅"),
    # storefront - 大学餐厅特例(走餐饮,不走 office)
    ("大学餐厅", "storefront", "学校餐厅"),
    ("餐厅", "storefront", "餐厅"),
    # storefront - 通用"店"字兜底(放最后,免误伤"学校"等不含"店"但前面没命中的)
    ("店", "storefront", "未知业态门面"),
]


def classify(project_id: str, line_items: list[dict]) -> tuple[BusinessLine, str, str]:
    """返回 (business_line, business_type, hit_keyword)。未命中返回 ('unknown', '', '')。"""
    # 优先 file name(信息密度最高)
    for kw, line, btype in RULES:
        if kw in project_id:
            return line, btype, kw

    # 兜底:扫前 30 条 line item 名(覆盖文件名抽象时的内部线索)
    item_text = " ".join(
        (it.get("item_name") or "") + " " + (it.get("category") or "")
        for it in line_items[:30]
    )
    for kw, line, btype in RULES:
        if kw in item_text:
            return line, btype, f"item:{kw}"

    return "unknown", "", ""


def load_manual_overrides(path: Path) -> dict[str, dict]:
    """加载店主人工修正的标签。

    WHY 设这一层覆盖:
    - 文件名只含通用词("店"/"坊")的项目,规则法和 LLM 都猜不到具体业态
    - 店主自己知道项目背景,但这种"私有知识"不该 hardcode 进 RULES(那是通用启发式)
    - 单独文件维护:Sprint 3 LLM 全量复跑时也以此为最高优先级,人工判断永远不被覆盖
    """
    if not path.exists():
        log.info("no manual overrides file at %s, skip", path)
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    overrides = data.get("overrides", {})
    log.info("loaded %d manual overrides from %s", len(overrides), path)
    return overrides


def load_manual_areas(path: Path) -> dict[str, float | None]:
    """加载店主回填的项目面积。

    WHY 单文件管理而非塞进 manual_overrides:
    - 面积是"店主凭印象估计"的尺度,精度低于 type/total(精度 ±20%);
      与 overrides 里的硬规则(必须精确)放一起会让 reviewer 误以为同等可靠
    - 面积可能在不同 Sprint 通过不同方式补全(店主→LLM→视觉),数据治理路径独立
    """
    if not path.exists():
        log.info("no manual areas file at %s, skip", path)
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("areas", {})
    # 兼容两种格式:{ pid: float } 或 { pid: { area_sqm: float, note: str } }
    areas: dict[str, float | None] = {}
    for pid, v in raw.items():
        if isinstance(v, dict):
            areas[pid] = v.get("area_sqm")
        else:
            areas[pid] = v
    filled = sum(1 for v in areas.values() if v is not None)
    log.info("loaded %d manual areas from %s (filled=%d)", len(areas), path, filled)
    return areas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects", default="data/projects.jsonl")
    ap.add_argument("--items", default="data/quotes.jsonl")
    ap.add_argument("--overrides", default="knowledge/manual_overrides.json")
    ap.add_argument("--areas", default="knowledge/manual_areas.json")
    ap.add_argument("--out", default="data/projects_labeled.jsonl")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    overrides = load_manual_overrides(Path(args.overrides))
    manual_areas = load_manual_areas(Path(args.areas))

    # 按 project_id 索引 line items,便于二次扫描
    items_by_project: dict[str, list[dict]] = {}
    for line in Path(args.items).read_text(encoding="utf-8").splitlines():
        it = json.loads(line)
        items_by_project.setdefault(it["project_id"], []).append(it)

    counter: Counter[BusinessLine] = Counter()
    by_source: Counter[str] = Counter()
    unknowns: list[str] = []

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fo:
        for line in Path(args.projects).read_text(encoding="utf-8").splitlines():
            project = json.loads(line)
            pid = project["project_id"]

            # 优先级 1:人工覆盖(店主直接告知)
            if pid in overrides:
                ov = overrides[pid]
                biz_line = ov["business_line"]
                biz_type = ov.get("business_type")
                hit = "manual"
                source = "manual"
                # WHY 可选 total_amount 覆盖:parse_quotes 启发式列名匹配对合并单元格抽不出
                # 合计,店主可在 overrides 里直接补,优先级最高
                if "total_amount" in ov and ov["total_amount"] is not None:
                    project["total_amount"] = float(ov["total_amount"])
                    project["total_amount_source"] = "manual"
            else:
                # 优先级 2:规则法
                biz_line, biz_type, hit = classify(pid, items_by_project.get(pid, []))
                source = "rule" if biz_line != "unknown" else "unknown"

            project["business_line"] = biz_line
            project["business_type"] = biz_type or None
            # WHY label_source 区分来源:Sprint 3 LLM 全量复跑时,manual 永不被覆盖、rule 可被改写
            project["label_source"] = source
            project["label_hint"] = hit or None

            # WHY 在 label 阶段合并 area_sqm:面积是店主回填的 manual 来源,与 type 同源同优先级,
            #     一并处理可避免 Sprint 1 收尾再多跑一个 stage(extract_area 仍负责自动扫描,
            #     这里只接 manual_areas 的最终结果)
            if pid in manual_areas and manual_areas[pid] is not None:
                area = float(manual_areas[pid])
                project["area_sqm"] = area
                project["area_source"] = "manual"
                total = project.get("total_amount")
                if total is not None and area > 0:
                    # WHY 整数:¥/㎡ 用作 Guardrail P10-P90 比较的标尺,小数位无信息
                    project["per_sqm_yuan"] = round(float(total) / area)
                    project["per_sqm_source"] = "manual_area + " + (project.get("total_amount_source") or "parse")

            fo.write(json.dumps(project, ensure_ascii=False) + "\n")
            counter[biz_line] += 1
            by_source[source] += 1
            if biz_line == "unknown":
                unknowns.append(pid)
            psm = project.get("per_sqm_yuan")
            log.info("%-50s → %-12s / %-12s (src=%s,hit=%s) area=%s ¥/㎡=%s",
                     pid[:50], biz_line, biz_type or "-", source, hit or "-",
                     project.get("area_sqm") or "-", psm or "-")

    log.info("")
    log.info("=== 业态汇总 ===")
    for line in ("residential", "office", "storefront", "unknown"):
        log.info("  %s: %d", line, counter[line])
    log.info("")
    log.info("=== 标签来源 ===")
    for src in ("manual", "rule", "unknown"):
        log.info("  %s: %d", src, by_source[src])
    if unknowns:
        log.info("")
        log.info("=== unknown 名单(待 LLM 兜底)===")
        for pid in unknowns:
            log.info("  - %s", pid)


if __name__ == "__main__":
    main()
