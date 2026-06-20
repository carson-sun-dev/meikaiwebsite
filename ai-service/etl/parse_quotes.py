"""
23 份历史报价 xls/xlsx → JSONL。

设计要点:
- 每份文件 ≈ 一个项目报价单;一份文件可能含多个 sheet,逐 sheet 抽取
- 不假设列结构统一(23 份格式差异很大),用"启发式列名匹配"找出"项目/数量/单价/小计"四要素
- LLM 打标(业态/档次/材料)推迟到 etl/label_with_llm.py(Sprint 1 后期);本脚本只产结构化原料
- 输出 quotes.jsonl,一行一条 line item;另产 projects.jsonl,一行一个项目级摘要

用法:
    python -m etl.parse_quotes --src "/Users/carrrson/developer/预算A" --out data/

依赖:pandas、openpyxl(xlsx)、xlrd==2.0(老 xls)。
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

log = logging.getLogger("etl.parse_quotes")

# 列名启发式:中文报价单常见叫法的同义词聚合
COLUMN_ALIASES: dict[str, list[str]] = {
    "item_name":  ["项目名称", "项目", "名称", "工程项目", "分项工程", "工程名称", "材料名称"],
    "spec":       ["规格", "型号", "规格型号", "材质", "品牌"],
    "unit":       ["单位"],
    "quantity":   ["数量", "工程量"],
    "unit_price": ["单价", "综合单价", "市场价"],
    "subtotal":   ["金额", "合价", "小计", "总价", "合计"],
    "category":   ["类别", "分类", "工程分类", "部位"],
    "remark":     ["备注", "说明"],
}


@dataclass
class LineItem:
    project_id: str           # 文件名(去扩展名)
    sheet: str
    row_idx: int
    item_name: str | None
    spec: str | None
    unit: str | None
    quantity: float | None
    unit_price: float | None
    subtotal: float | None
    category: str | None
    remark: str | None
    raw_row: dict[str, Any]   # 兜底,LLM 打标时如启发式失败可回看原始行


@dataclass
class ProjectSummary:
    project_id: str
    source_file: str
    sheet_count: int
    line_item_count: int
    total_amount: float | None
    # 以下字段 Sprint 1 后期 LLM 打标补:
    business_line: str | None = None     # residential | office | storefront
    business_type: str | None = None     # 火锅/咖啡/眼镜店/办公...
    tier: str | None = None              # basic | mid | premium
    area_sqm: float | None = None
    per_sqm_yuan: float | None = None


# ---------- 工具 ----------

def normalize_header(s: Any) -> str:
    """归一化表头:去空格 + 去括号注解。

    WHY 去括号:23 份预算单里大量列名带单位注解 — "金额（元）" / "单价(元)" / "数量（M2）",
    括号内是单位说明对语义无影响。早期版本不剥括号导致 6 个项目(住宅、办公为主)
    抽到 0 个 line item subtotal,空间分项 ETL 直接没数据可聚合(发现于 2026-06-08 ETL
    Sprint 2 step 2),这是个静默数据丢失 bug。
    """
    if s is None:
        return ""
    norm = re.sub(r"\s+", "", str(s)).strip()
    # 中英文括号都剥(含内容)
    return re.sub(r"[（(][^）)]*[）)]", "", norm)


def map_columns(headers: list[str]) -> dict[str, str]:
    """把启发式同义词映射到标准字段名;返回 {standard_field: original_col_name}"""
    out: dict[str, str] = {}
    norm_headers = {normalize_header(h): h for h in headers}
    for std, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in norm_headers:
                out[std] = norm_headers[alias]
                break
    return out


def safe_float(v: Any) -> float | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        # 处理 "1,234.56" / "￥123" / "123元" 等脏数据
        s = re.sub(r"[^\d.\-]", "", str(v))
        return float(s) if s else None
    except (ValueError, TypeError):
        return None


def safe_str(v: Any) -> str | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    return s or None


# ---------- 主流程 ----------

def parse_sheet(project_id: str, sheet_name: str, df: pd.DataFrame) -> list[LineItem]:
    """单 sheet → line items。找不到表头时跳过本 sheet。"""
    # 启发式表头探测:扫前 10 行,找含 ≥3 个 alias 命中的那一行作表头
    header_row = None
    best_hits = 0
    for i in range(min(10, len(df))):
        cells = [normalize_header(c) for c in df.iloc[i].tolist()]
        hits = sum(1 for c in cells if any(c == a for aliases in COLUMN_ALIASES.values() for a in aliases))
        if hits > best_hits:
            best_hits = hits
            header_row = i
    if header_row is None or best_hits < 3:
        log.debug("[%s/%s] no header found (best_hits=%d), skip", project_id, sheet_name, best_hits)
        return []

    headers = [normalize_header(c) for c in df.iloc[header_row].tolist()]
    data = df.iloc[header_row + 1 :].reset_index(drop=True)
    data.columns = headers

    colmap = map_columns(headers)
    if "item_name" not in colmap:
        log.debug("[%s/%s] no item_name column, skip", project_id, sheet_name)
        return []

    items: list[LineItem] = []
    for idx, row in data.iterrows():
        name = safe_str(row.get(colmap["item_name"]))
        if not name:
            continue
        items.append(
            LineItem(
                project_id=project_id,
                sheet=sheet_name,
                row_idx=int(idx),
                item_name=name,
                spec=safe_str(row.get(colmap.get("spec"))) if "spec" in colmap else None,
                unit=safe_str(row.get(colmap.get("unit"))) if "unit" in colmap else None,
                quantity=safe_float(row.get(colmap.get("quantity"))) if "quantity" in colmap else None,
                unit_price=safe_float(row.get(colmap.get("unit_price"))) if "unit_price" in colmap else None,
                subtotal=safe_float(row.get(colmap.get("subtotal"))) if "subtotal" in colmap else None,
                category=safe_str(row.get(colmap.get("category"))) if "category" in colmap else None,
                remark=safe_str(row.get(colmap.get("remark"))) if "remark" in colmap else None,
                raw_row={str(k): str(v) for k, v in row.to_dict().items()},
            )
        )
    return items


def parse_file(path: Path) -> tuple[list[LineItem], ProjectSummary]:
    project_id = path.stem.strip().replace(" ", "_")
    log.info("parsing %s", path.name)

    # xlrd 2.0 不再支持 xlsx,pandas 会自动选 engine;老 xls 显式指定
    engine = "xlrd" if path.suffix.lower() == ".xls" else "openpyxl"
    try:
        sheets: dict[str, pd.DataFrame] = pd.read_excel(path, sheet_name=None, header=None, engine=engine)
    except Exception as e:
        log.error("failed to read %s: %s", path.name, e)
        return [], ProjectSummary(project_id=project_id, source_file=path.name,
                                  sheet_count=0, line_item_count=0, total_amount=None)

    all_items: list[LineItem] = []
    for sheet_name, df in sheets.items():
        items = parse_sheet(project_id, sheet_name, df)
        all_items.extend(items)

    total = sum((i.subtotal or 0.0) for i in all_items) or None
    summary = ProjectSummary(
        project_id=project_id,
        source_file=path.name,
        sheet_count=len(sheets),
        line_item_count=len(all_items),
        total_amount=total,
    )
    return all_items, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="历史报价 xls/xlsx 目录")
    ap.add_argument("--out", default="data", help="JSONL 输出目录")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")

    src = Path(args.src).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    # WHY 排除 meikai_* 前缀:本项目自己写到 预算A/ 的辅助模板(如 meikai_areas_to_fill.xlsx)
    #     不是历史报价单,扫到会污染 projects.jsonl
    files = sorted([
        p for p in src.iterdir()
        if p.suffix.lower() in (".xls", ".xlsx") and not p.stem.startswith("meikai_")
    ])
    log.info("found %d files in %s", len(files), src)

    items_path = out / "quotes.jsonl"
    proj_path  = out / "projects.jsonl"

    total_items = 0
    with items_path.open("w", encoding="utf-8") as fi, proj_path.open("w", encoding="utf-8") as fp:
        for f in files:
            items, summary = parse_file(f)
            for it in items:
                fi.write(json.dumps(asdict(it), ensure_ascii=False) + "\n")
            fp.write(json.dumps(asdict(summary), ensure_ascii=False) + "\n")
            total_items += len(items)
            log.info("  → %d line items, total=%s", len(items), summary.total_amount)

    log.info("done: %d projects, %d line items → %s", len(files), total_items, out)


if __name__ == "__main__":
    main()
