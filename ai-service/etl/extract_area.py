"""
从 23 份历史预算 xls/xlsx 里抽"工程总面积",作为 ¥/㎡ 分位数计算的分母。

WHY 单独写一个 extractor 而不复用 parse_quotes:
- parse_quotes.py 的 COLUMN_ALIASES 是结构化"列名→字段"映射,
  只识别表头里的"数量/单价/合价"等;
- 面积通常**不在表头**,而是写在 sheet 顶部的"工程概况"标题区、
  合并单元格里、或者备注里(自由文本),需要不同的扫描策略
- 扫描全表所有 cell 的字符串内容,用正则抓"面积: XXX㎡"模式

WHY 此修复:Sprint 1 收尾时 aggregate.py 用 total_amount 凑了表面交付,
但 DESIGN §3 明确要求 P25/P50/P75 ¥/㎡ —— 没有面积分母,Guardrail 输出侧
就拿不到合理参考(详见 §16 缺陷复盘)。

用法:
    python -m etl.extract_area --src "/Users/carrrson/developer/预算A" --out data/extracted_areas.json
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

import pandas as pd

log = logging.getLogger("etl.extract_area")

# WHY 模式覆盖多种叫法:中文装修预算单"面积"字段没统一规范,
#     常见叫法:总面积/建筑面积/施工面积/装修面积/使用面积/室内面积/铺装面积
# 单位:㎡ / 平米 / 平方米 / 平方 / m²
AREA_PATTERNS = [
    # "总面积: 280㎡" / "建筑面积: 280 平米" / "面积:280 m²"
    re.compile(r"(?:总|建筑|施工|装修|使用|室内|铺装)?\s*面积\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(?:㎡|平米|平方米|平方|m²|m2)", re.IGNORECASE),
    # "280㎡" 紧贴 sheet 顶部的项目概况(更宽松,放后面避免误抓 line item 里的 16.8㎡)
    re.compile(r"^\s*(?:.*?[:：])?\s*(\d{2,5}(?:\.\d+)?)\s*(?:㎡|平米|平方米|平方|m²|m2)\s*[\)）]?$", re.IGNORECASE),
]

# WHY 只扫前 15 行 + 末尾 10 行:面积通常出现在"工程概况"(表头前)或"合计签字"(表末)
HEAD_ROWS = 15
TAIL_ROWS = 10
# 面积合理范围:< 20㎡ 大概率是 line item 数量(地砖 16.8㎡),> 5000 大概率是户型注释
MIN_PLAUSIBLE_AREA = 20.0
MAX_PLAUSIBLE_AREA = 5000.0


def extract_from_text(text: str) -> float | None:
    """从一段文本里抽面积。返回首个合理值或 None。"""
    if not text or pd.isna(text):
        return None
    s = str(text).strip()
    for pat in AREA_PATTERNS:
        for m in pat.finditer(s):
            try:
                v = float(m.group(1))
            except (ValueError, IndexError):
                continue
            if MIN_PLAUSIBLE_AREA <= v <= MAX_PLAUSIBLE_AREA:
                return v
    return None


def scan_sheet(df: pd.DataFrame) -> tuple[float | None, str | None]:
    """扫单 sheet 的头尾区域,返回 (area, hit_cell_text) 或 (None, None)。"""
    n = len(df)
    if n == 0:
        return None, None

    rows_to_scan = list(range(min(HEAD_ROWS, n))) + list(range(max(n - TAIL_ROWS, HEAD_ROWS), n))
    for i in rows_to_scan:
        row = df.iloc[i]
        for v in row.tolist():
            area = extract_from_text(v)
            if area is not None:
                return area, str(v)[:100]
    return None, None


def parse_file(path: Path) -> tuple[float | None, str | None]:
    """打开 xls,逐 sheet 扫,返回 (area, hit_text) 或 (None, None)。"""
    engine = "xlrd" if path.suffix.lower() == ".xls" else "openpyxl"
    try:
        sheets: dict[str, pd.DataFrame] = pd.read_excel(
            path, sheet_name=None, header=None, engine=engine
        )
    except Exception as e:
        log.error("failed to read %s: %s", path.name, e)
        return None, None

    for sheet_name, df in sheets.items():
        area, hit = scan_sheet(df)
        if area is not None:
            log.info("  [%s] hit=%r → %.1f ㎡", sheet_name, hit, area)
            return area, hit
    return None, None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="历史预算 xls/xlsx 目录")
    ap.add_argument("--out", default="data/extracted_areas.json")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    src = Path(args.src).expanduser().resolve()
    files = sorted([p for p in src.iterdir() if p.suffix.lower() in (".xls", ".xlsx")])
    log.info("scanning %d files", len(files))

    results: dict[str, dict] = {}
    found = missed = 0

    for f in files:
        # WHY project_id 计算口径必须与 parse_quotes.py 完全一致,否则下游 join 不上
        project_id = f.stem.strip().replace(" ", "_")
        log.info("=== %s ===", f.name)
        area, hit = parse_file(f)
        results[project_id] = {
            "source_file": f.name,
            "area_sqm": area,
            "hit_text": hit,
        }
        if area is not None:
            found += 1
        else:
            missed += 1
            log.info("  (no area found)")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log.info("")
    log.info("=== 汇总 ===")
    log.info("  自动抓到面积: %d / %d", found, len(files))
    log.info("  需手工补全:  %d / %d", missed, len(files))
    log.info("  写入: %s", args.out)


if __name__ == "__main__":
    main()
