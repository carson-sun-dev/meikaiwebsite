"""
OCR Provider 抽象。DESIGN §4.10:
- 本地完整版主路径:PaddleOCR 本地
- 生产 2C4G 路径:百度 OCR API(主)/ 阿里 / Doubao(备选)
- Sprint 1 默认走 Mock,返回空文本块

业务代码严禁直接 import 具体实现,只能 `get_ocr_client()`。
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache
from typing import Protocol

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.config import get_settings

log = logging.getLogger("infra.ocr")


@dataclass
class OcrBlock:
    text: str
    bbox: tuple[float, float, float, float] | None = None   # (x1, y1, x2, y2)
    confidence: float = 0.0


class OCRClient(Protocol):
    async def recognize(self, image_bytes: bytes) -> list[OcrBlock]: ...

    @property
    def name(self) -> str: ...


class MockOCR:
    """返回空块,验证管线连通。Sprint 1 默认。"""

    name = "mock"

    async def recognize(self, image_bytes: bytes) -> list[OcrBlock]:
        return []


class LocalPaddleOCR:
    """本地 PaddleOCR。Lazy import,首次约耗 1-2 GB 峰值内存。"""

    name = "paddleocr"

    def __init__(self) -> None:
        self._ocr = None  # type: ignore[assignment]

    def _load(self) -> None:
        if self._ocr is not None:
            return
        try:
            from paddleocr import PaddleOCR  # type: ignore[import-not-found]
        except ImportError as e:
            raise RuntimeError(
                "OCR_PROVIDER=local_paddleocr 需要安装 local extras:"
                "  pip install -e '.[local]'"
            ) from e
        log.info("loading PaddleOCR (lazy)")
        self._ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

    async def recognize(self, image_bytes: bytes) -> list[OcrBlock]:
        self._load()
        assert self._ocr is not None
        import asyncio
        import io

        from PIL import Image  # PaddleOCR 输入支持 numpy/path,这里转 numpy

        def _run() -> list[OcrBlock]:
            import numpy as np
            img = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            result = self._ocr.ocr(img, cls=True)  # type: ignore[union-attr]
            blocks: list[OcrBlock] = []
            for line in (result[0] or []):
                bbox_pts, (text, conf) = line
                xs = [p[0] for p in bbox_pts]
                ys = [p[1] for p in bbox_pts]
                blocks.append(OcrBlock(
                    text=text,
                    bbox=(min(xs), min(ys), max(xs), max(ys)),
                    confidence=float(conf),
                ))
            return blocks

        return await asyncio.to_thread(_run)


class BaiduOCR:
    """百度 OCR API(高精度版)。生产 2C4G 主路径。

    Sprint 3 接入:Token 走 client_credentials 流程,这里 stub 实现。
    """

    name = "baidu-ocr"

    def __init__(self, api_key: str, secret_key: str) -> None:
        self._api_key = api_key
        self._secret_key = secret_key
        self._client = httpx.AsyncClient(timeout=15.0)
        self._token: str | None = None

    async def _ensure_token(self) -> str:
        if self._token:
            return self._token
        resp = await self._client.post(
            "https://aip.baidubce.com/oauth/2.0/token",
            params={
                "grant_type": "client_credentials",
                "client_id": self._api_key,
                "client_secret": self._secret_key,
            },
        )
        resp.raise_for_status()
        self._token = resp.json()["access_token"]
        return self._token  # type: ignore[return-value]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def recognize(self, image_bytes: bytes) -> list[OcrBlock]:
        import base64
        token = await self._ensure_token()
        resp = await self._client.post(
            "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate",
            params={"access_token": token},
            data={"image": base64.b64encode(image_bytes).decode()},
        )
        resp.raise_for_status()
        words = resp.json().get("words_result", [])
        return [OcrBlock(text=w["words"]) for w in words]


@lru_cache
def get_ocr_client() -> OCRClient:
    s = get_settings()
    provider = s.ocr_provider

    if provider == "mock" or s.llm_mode == "mock":
        return MockOCR()
    if provider == "local_paddleocr":
        return LocalPaddleOCR()
    if provider == "baidu":
        if not (s.baidu_ocr_api_key and s.baidu_ocr_secret_key):
            log.warning("OCR_PROVIDER=baidu but BAIDU_OCR_* missing,降级为 mock")
            return MockOCR()
        return BaiduOCR(s.baidu_ocr_api_key, s.baidu_ocr_secret_key)
    if provider in ("aliyun", "doubao"):
        # Sprint 3 再补,目前先走 mock
        log.warning("OCR_PROVIDER=%s 尚未实现,临时走 mock", provider)
        return MockOCR()

    raise ValueError(f"unknown OCR_PROVIDER: {provider}")
