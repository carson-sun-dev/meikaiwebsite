"""
LLM 客户端抽象 + 火山方舟 live 实现。

DESIGN §4.2 多级路由策略(2026-06 统一火山方舟后简化为两级):
- L0:Doubao-1.5-lite-32k —— 意图分类 / 闲聊判别 / ETL 打标(成本最低,~¥0.0003/k token)
- L2:DeepSeek-V3.2       —— 核心多轮对话 + 复杂报价(质量最高,~¥0.5/M in)

业务代码经 `get_llm_client()` 拿到 client,调用 `stream(msg, level="l0"|"l2")`。
Sprint 4 升级 V3.2→V4 时只改 .env 的 endpoint ID,业务代码零改动。
"""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Literal, Protocol

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.config import get_settings

log = logging.getLogger("infra.llm_client")

Level = Literal["l0", "l2"]


class LLMClient(Protocol):
    async def stream(self, user_msg: str, level: Level = "l2") -> AsyncIterator[str]: ...

    @property
    def name(self) -> str: ...


class MockLLM:
    """逐字流出固定模板,验证 SSE 端到端;不消耗任何 token。"""

    name = "mock"

    async def stream(self, user_msg: str, level: Level = "l2") -> AsyncIterator[str]:
        reply = (
            f"【mock 回复 / level={level}】我收到您的消息:「{user_msg[:80]}」。"
            "切 LLM_MODE=live 后将替换为真实推理。"
        )
        for ch in reply:
            await asyncio.sleep(0.01)
            yield ch


class VolcArkLLM:
    """火山方舟 OpenAI 兼容流式客户端。

    WHY 不用现成的 openai SDK:火山方舟 endpoint ID 作 model 字段、错误码与官方 OpenAI 略有差异,
    且我们只需要 chat/completions 一个 endpoint + 简单 SSE 解析,自建 ~50 行更轻,
    省去 openai SDK 全量依赖(~10MB)与版本耦合。
    """

    name = "volc-ark"

    def __init__(
        self,
        api_key: str,
        base_url: str,
        lite_endpoint: str,
        deepseek_endpoint: str,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=60.0,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._endpoints: dict[Level, str] = {
            "l0": lite_endpoint,
            "l2": deepseek_endpoint,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        # WHY 只重试网络/5xx,不重试 400/401:鉴权失败重试也没用,反而拖慢失败暴露
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True,
    )
    async def _request_stream(self, endpoint: str, user_msg: str) -> httpx.Response:
        return await self._client.send(
            self._client.build_request(
                "POST", "/chat/completions",
                json={
                    "model": endpoint,
                    "messages": [{"role": "user", "content": user_msg}],
                    "stream": True,
                },
            ),
            stream=True,
        )

    async def stream(self, user_msg: str, level: Level = "l2") -> AsyncIterator[str]:
        endpoint = self._endpoints.get(level)
        if not endpoint:
            raise RuntimeError(
                f"LLM endpoint for level={level!r} 未配置;"
                f"请检查 .env 的 DOUBAO_LITE_ENDPOINT / DEEPSEEK_ENDPOINT"
            )

        resp = await self._request_stream(endpoint, user_msg)
        try:
            resp.raise_for_status()
            # WHY 手动解 SSE 而非用第三方库:格式简单(data: {json}\n\n),解析逻辑 < 10 行
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    data = json.loads(payload)
                    delta = data["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError):
                    # 容忍单条 chunk 异常,不打断整条流
                    continue
        finally:
            await resp.aclose()


@lru_cache
def get_llm_client() -> LLMClient:
    s = get_settings()
    if s.llm_mode == "mock":
        return MockLLM()
    if not s.doubao_api_key:
        log.warning("LLM_MODE=live but DOUBAO_API_KEY missing,降级为 mock")
        return MockLLM()
    if not (s.doubao_lite_endpoint and s.deepseek_endpoint):
        log.warning("LLM_MODE=live but L0/L2 endpoint 未全配置,降级为 mock")
        return MockLLM()
    return VolcArkLLM(
        api_key=s.doubao_api_key,
        base_url=s.doubao_base_url,
        lite_endpoint=s.doubao_lite_endpoint,
        deepseek_endpoint=s.deepseek_endpoint,
    )
