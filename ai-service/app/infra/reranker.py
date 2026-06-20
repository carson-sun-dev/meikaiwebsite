"""
Reranker Provider 抽象。DESIGN §4.9:
- 本地完整版主路径:bge-reranker-v2-m3 本地(~568 MB)
- 生产 2C4G 路径:火山方舟 reranker API
- Sprint 1 默认走 Mock,验证 Hybrid Search → rerank → trim 管道连通

业务代码严禁直接 import 具体实现,只能 `get_reranker_client()`。
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Protocol

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.config import get_settings

log = logging.getLogger("infra.reranker")


class RerankerClient(Protocol):
    async def rerank(self, query: str, docs: list[str], top_k: int) -> list[tuple[int, float]]:
        """返回 [(doc_index, score), ...] 按 score 降序,长度 ≤ top_k。"""
        ...

    @property
    def name(self) -> str: ...


class MockReranker:
    """按字面匹配度打分,不调任何模型。Sprint 1 默认。"""

    name = "mock"

    async def rerank(self, query: str, docs: list[str], top_k: int) -> list[tuple[int, float]]:
        q_tokens = set(query)
        scored = [
            (i, len(q_tokens & set(d)) / max(len(q_tokens), 1))
            for i, d in enumerate(docs)
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


class LocalBgeReranker:
    """本地 bge-reranker-v2-m3。Lazy import,需要 .[local] extras。"""

    name = "bge-reranker-v2-m3"

    def __init__(self) -> None:
        self._model = None  # type: ignore[assignment]

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from FlagEmbedding import FlagReranker  # type: ignore[import-not-found]
        except ImportError as e:
            raise RuntimeError(
                "RERANKER_PROVIDER=local_bge_reranker 需要安装 local extras:"
                "  pip install -e '.[local]'"
            ) from e
        log.info("loading bge-reranker-v2-m3 weights")
        self._model = FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)

    async def rerank(self, query: str, docs: list[str], top_k: int) -> list[tuple[int, float]]:
        self._load()
        assert self._model is not None
        import asyncio
        pairs = [[query, d] for d in docs]
        scores = await asyncio.to_thread(self._model.compute_score, pairs, normalize=True)
        scored = list(enumerate(scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [(i, float(s)) for i, s in scored[:top_k]]


class VolcReranker:
    """火山方舟 reranker API。生产 2C4G 主路径。"""

    name = "volc-reranker"

    def __init__(self, api_key: str, base_url: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=15.0,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def rerank(self, query: str, docs: list[str], top_k: int) -> list[tuple[int, float]]:
        # TODO Sprint 3 核对火山方舟 reranker 实际 endpoint 与请求体
        resp = await self._client.post("/rerank", json={
            "model": "doubao-reranker",
            "query": query,
            "documents": docs,
            "top_n": top_k,
        })
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [(r["index"], float(r["relevance_score"])) for r in results]


@lru_cache
def get_reranker_client() -> RerankerClient:
    s = get_settings()
    provider = s.reranker_provider

    if provider == "mock" or s.llm_mode == "mock":
        return MockReranker()
    if provider == "local_bge_reranker":
        return LocalBgeReranker()
    if provider == "volc":
        if not s.volc_reranker_api_key:
            log.warning("RERANKER_PROVIDER=volc but VOLC_RERANKER_API_KEY missing,降级为 mock")
            return MockReranker()
        return VolcReranker(s.volc_reranker_api_key, s.volc_reranker_base_url)

    raise ValueError(f"unknown RERANKER_PROVIDER: {provider}")
