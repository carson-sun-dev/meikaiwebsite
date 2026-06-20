"""
data/quotes.jsonl → Qdrant collection: quote_items
data/faq_corpus/*.md → Qdrant collection: knowledge_faq(Sprint 1 后期补,先占位)

用法:
    python -m etl.build_index --quotes data/quotes.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
from pathlib import Path

from app.infra.qdrant_client import ensure_collections, upsert_quote_items

log = logging.getLogger("etl.build_index")


async def index_quotes(path: Path, batch_size: int = 200) -> int:
    await ensure_collections()
    total = 0
    buf: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        buf.append(json.loads(line))
        if len(buf) >= batch_size:
            total += await upsert_quote_items(buf)
            buf.clear()
            log.info("indexed %d so far", total)
    if buf:
        total += await upsert_quote_items(buf)
    return total


async def main_async() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", default="data/quotes.jsonl")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    n = await index_quotes(Path(args.quotes))
    log.info("done: %d line items into quote_items", n)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
