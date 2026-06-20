"""
LLM 兜底打标:给 label_rule_based.py 漏判的项目用 L0 (Doubao-1.5-lite) 推断业态。

WHY 用 L0 而非 L2:
- 任务简单(从文件名+10 条样例条目推 3 选 1 业态),L0 准确率与 L2 几乎无差
- 单次调用成本 ~¥0.0003 vs L2 ~¥0.005,便宜 15 倍
- 23 个项目全跑 L0 也不到 1 分钱

WHY 只补 unknown 而非全跑:
- 规则法命中的 21 个已经 99% 正确(文件名直接含业态词),LLM 可能反而引入噪音
- Sprint 3 想全量 LLM 复跑时去掉 --only-unknown 参数即可

WHY 原地覆盖 projects_labeled.jsonl:
- 写时先到 .tmp 再 atomic rename,中途断网不破坏原文件
- label_source 字段区分来源:rule / llm / unknown,Sprint 3 复跑时可按来源决策保留或覆盖

用法(必须 LLM_MODE=live + key 配齐):
    LLM_MODE=live python -m etl.label_with_llm --only-unknown
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import re
from pathlib import Path

from app.infra.llm_client import get_llm_client

log = logging.getLogger("etl.label_with_llm")

# WHY prompt 极简严格 JSON:L0 模型按 prompt 长度计费,且 strict JSON 解析容错性最高
# 三个枚举值与 label_rule_based.py 对齐,Sprint 2 Router 直接读
PROMPT_TEMPLATE = """你是装修预算分析师。根据下面信息判断项目业态,只输出 JSON,不要任何其他文字。

业态(三选一):
- residential: 住宅(家装/别墅/公寓/小区房)
- office: 办公(办公室/写字楼/学校/教室/科技园)
- storefront: 门面店铺(餐饮/零售/服务等商业空间)

文件名:{filename}
样例条目(前 10 条):
{sample}

输出格式(严格 JSON,无其他文字):
{{"business_line": "residential|office|storefront", "business_type": "中文细分如 火锅店/办公室/住宅小区"}}"""


def extract_json(text: str) -> dict:
    """从模型输出里抠 JSON。L0 偶尔会带 ``` 包裹或额外解释,这里宽容处理。"""
    # 优先找 ```json ... ``` 块
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # 退路:第一个 {...} 块
    m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON in LLM output: {text[:200]}")
    return json.loads(m.group(0))


async def label_one(llm, project: dict, items: list[dict]) -> dict | None:
    sample = "\n".join(
        f"- {it.get('item_name','?')} / {it.get('spec') or '-'} / 小计 {it.get('subtotal') or '-'}"
        for it in items[:10]
    )
    prompt = PROMPT_TEMPLATE.format(
        filename=project["source_file"],
        sample=sample,
    )

    out_buf: list[str] = []
    async for ch in llm.stream(prompt, level="l0"):
        out_buf.append(ch)
    raw = "".join(out_buf).strip()

    try:
        return extract_json(raw)
    except (ValueError, json.JSONDecodeError) as e:
        log.warning("[%s] failed to parse: %s | raw=%r", project["project_id"], e, raw[:150])
        return None


async def main_async() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="data/projects_labeled.jsonl")
    ap.add_argument("--items", default="data/quotes.jsonl")
    ap.add_argument("--only-unknown", action="store_true",
                    help="只对 business_line=='unknown' 的行调 LLM(推荐)")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    llm = get_llm_client()
    if llm.name == "mock":
        log.error("LLM 走 mock,真打标无意义。请设 LLM_MODE=live + 火山方舟 key 与 endpoint")
        raise SystemExit(2)
    log.info("LLM client: %s", llm.name)

    # 索引 items
    items_by_project: dict[str, list[dict]] = {}
    for line in Path(args.items).read_text(encoding="utf-8").splitlines():
        it = json.loads(line)
        items_by_project.setdefault(it["project_id"], []).append(it)

    src_path = Path(args.src)
    tmp_path = src_path.with_suffix(".jsonl.tmp")

    # 计数 + 跳过策略
    processed = updated = 0
    with tmp_path.open("w", encoding="utf-8") as fo:
        for line in src_path.read_text(encoding="utf-8").splitlines():
            project = json.loads(line)
            processed += 1
            need_llm = (
                project.get("business_line") in (None, "unknown")
                if args.only_unknown else True
            )
            if not need_llm:
                fo.write(json.dumps(project, ensure_ascii=False) + "\n")
                continue

            log.info("LLM labeling: %s", project["project_id"])
            labels = await label_one(llm, project, items_by_project.get(project["project_id"], []))
            if labels:
                project["business_line"] = labels.get("business_line") or "unknown"
                project["business_type"] = labels.get("business_type") or None
                project["label_source"] = "llm"
                updated += 1
                log.info("  → %s / %s", project["business_line"], project["business_type"])
            else:
                log.warning("  → 保留 unknown")
            fo.write(json.dumps(project, ensure_ascii=False) + "\n")

    # atomic rename
    tmp_path.replace(src_path)
    log.info("done: %d processed, %d updated by LLM", processed, updated)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
