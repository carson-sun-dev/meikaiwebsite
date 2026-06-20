"""
稠密 Embedding Provider 抽象。DESIGN §2.3 / §4.8:
- 本地完整版主路径:bge-m3 本地(1024d)
- 生产 2C4G 路径:Doubao-embedding API
- Sprint 1 默认走 Mock,避免下载权重 / 调外网

业务代码严禁直接 import 具体实现,只能 `get_embedding_client()`。
"""
from __future__ import annotations

import hashlib
import logging
from functools import lru_cache
from typing import Protocol

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.config import get_settings

log = logging.getLogger("infra.embedding")

DENSE_DIM = 1024   # bge-m3 与 Doubao-embedding 当前选型同维度,迁移时需重灌 Qdrant


class EmbeddingClient(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...

    @property
    def name(self) -> str: ...


class MockEmbedding:
    """SHA256 → 1024d float ∈ [-1,1],determinstic。Sprint 1 默认,验证管线零成本。"""

    name = "mock"

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_vec(t) for t in texts]

    @staticmethod
    def _hash_vec(text: str) -> list[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        floats = [(b / 128.0) - 1.0 for b in h]
        rep = (DENSE_DIM + len(floats) - 1) // len(floats)
        return (floats * rep)[:DENSE_DIM]


class LocalBgeM3:
    """本地 bge-m3(FlagEmbedding)。Lazy import,模块加载不触发权重下载。

    需 `pip install -e .[local]` 才有 FlagEmbedding 依赖。
    首次调用时 lazy load,耗内存约 2.3 GB(FP32)。
    """

    name = "bge-m3"

    def __init__(self) -> None:
        self._model = None  # type: ignore[assignment]

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from FlagEmbedding import BGEM3FlagModel  # type: ignore[import-not-found]
        except ImportError as e:
            raise RuntimeError(
                "EMBEDDING_PROVIDER=local_bge_m3 需要安装 local extras:"
                "  pip install -e '.[local]'"
            ) from e
        log.info("loading bge-m3 weights (lazy,首次约需 10-30s)")
        self._model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        self._load()
        assert self._model is not None
        # FlagEmbedding 同步 API,这里用 to_thread 避免阻塞事件循环
        import asyncio
        out = await asyncio.to_thread(self._model.encode, texts, batch_size=8, max_length=512)
        return out["dense_vecs"].tolist()


class DoubaoEmbedding:
    """火山方舟 Doubao-embedding。OpenAI 兼容,POST /embeddings。生产 2C4G 主路径。

    WHY 用 endpoint ID 作 model 字段:火山方舟「在线推理」是项目级资源寻址机制,
    不同租户的 ID 不同,不能硬编码模型名(详见 config.py 同名注释)。
    """

    name = "doubao-embedding"

    def __init__(self, api_key: str, base_url: str, endpoint_id: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=30.0,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._endpoint = endpoint_id

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def embed(self, texts: list[str]) -> list[list[float]]:
        resp = await self._client.post("/embeddings", json={
            "model": self._endpoint,
            "input": texts,
        })
        resp.raise_for_status()
        data = resp.json()["data"]
        return [d["embedding"] for d in data]


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    s = get_settings()
    provider = s.embedding_provider

    if provider == "mock" or s.llm_mode == "mock":
        return MockEmbedding()
    if provider == "local_bge_m3":
        return LocalBgeM3()
    if provider == "doubao":
        if not (s.doubao_api_key and s.doubao_embedding_endpoint):
            log.warning("EMBEDDING_PROVIDER=doubao 缺 key 或 embedding_endpoint,降级为 mock")
            return MockEmbedding()
        return DoubaoEmbedding(s.doubao_api_key, s.doubao_base_url, s.doubao_embedding_endpoint)

    raise ValueError(f"unknown EMBEDDING_PROVIDER: {provider}")
