"""
FastAPI 入口。Sprint 2 step 1:/api/ai/chat 走 LangGraph(router → 三大 SubGraph)+ SSE 流式。
"""
import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from app.config import get_settings
from app.graphs import build_graph
from app.infra.checkpointer import open_checkpointer

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("ai-service")

# 全局并发闸 — DESIGN §11.1,2GB 机器下不能让 SSE 无限堆
session_sem = asyncio.Semaphore(settings.max_concurrent_sessions)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Sprint 2 step 6:lifespan 内启动 checkpointer + 编译图。

    WHY 把 saver 与 graph 都挂 app.state:
    - checkpointer 是 async ctx mgr,生命周期 = FastAPI 生命周期,enter/exit 必须在 lifespan
    - graph 编译产物含 saver 引用,不能在 lifespan 外提前编译(saver 还没准备好)
    - app.state 是 FastAPI 标准挂点,Request.app.state 端点侧可直接读
    """
    log.info("ai-service starting; llm_mode=%s ocr=%s", settings.llm_mode, settings.ocr_provider)
    async with open_checkpointer() as saver:
        app.state.checkpointer = saver
        # WHY 编译走拓扑校验 + 节点签名检查,有错应该在启动就暴露而非首次请求
        app.state.graph = build_graph(checkpointer=saver)
        log.info("graph compiled with checkpointer=%s", type(saver).__name__)
        yield
    log.info("ai-service stopping")


app = FastAPI(title="meikai ai-service", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"ok": True, "llm_mode": settings.llm_mode}


@app.post("/api/ai/chat")
async def chat(req: Request):
    """SSE 流式回复:LangGraph 编排 router → SubGraph,SubGraph 通过 stream_writer 推 L2 token。

    SSE event 协议:
    - meta:  路由结果 / 会话 ID 等元信息
    - delta: 一个 token 片段(text 字段)
    - done:  本轮结束
    - error: 异常(包括 busy/internal)
    """
    body = await req.json()
    user_msg = (body.get("message") or "").strip()
    conv_id = body.get("conversation_id") or str(uuid.uuid4())

    async def event_stream():
        acquired = False
        try:
            try:
                await asyncio.wait_for(session_sem.acquire(), timeout=0.1)
                acquired = True
            except asyncio.TimeoutError:
                yield {"event": "error", "data": json.dumps({"code": "busy", "msg": "系统繁忙,请稍后再试"})}
                return

            if not user_msg:
                yield {"event": "error", "data": json.dumps({"code": "empty", "msg": "消息为空"})}
                return

            yield {"event": "meta", "data": json.dumps({"conversation_id": conv_id})}

            graph = req.app.state.graph
            initial = {"conversation_id": conv_id, "user_msg": user_msg}

            # Sprint 2 step 6:thread_id=conversation_id 让 checkpointer 跨轮持久化 state
            # WHY 复用前端 conversation_id 作 thread_id:
            #     - 前端已有会话标识,不再造概念
            #     - 同一会话连续两轮 curl 走相同 thread → checkpointer 自动加载上轮 state
            #       (router.business_line + slots 都跨轮可见)
            config = {"configurable": {"thread_id": conv_id}}

            # WHY stream_mode=["updates", "custom"]:
            # - updates 给 router 落定后的 business_line(让前端可显示"已识别为门面房...")
            # - custom 拿 SubGraph 内部 stream_writer 推的 token 片段
            # 两路 yield 的是 (mode, payload) 元组,在外层分发到不同 SSE event 类型
            try:
                async for mode, payload in graph.astream(
                    initial,
                    config=config,
                    stream_mode=["updates", "custom"],
                ):
                    if await req.is_disconnected():
                        log.info("client disconnected, abort stream")
                        break

                    if mode == "updates" and isinstance(payload, dict):
                        # updates 形如 {"router": {"business_line": "storefront"}}
                        if "router" in payload:
                            bl = payload["router"].get("business_line")
                            yield {"event": "meta", "data": json.dumps({"business_line": bl})}
                        # SubGraph 落定时也会触发 updates(含 final_text),不必额外推送
                    elif mode == "custom" and isinstance(payload, dict):
                        kind = payload.get("kind", "delta")
                        if kind == "delta":
                            yield {"event": "delta", "data": json.dumps({"text": payload.get("text", "")})}

            except Exception:
                log.exception("graph stream failed")
                yield {"event": "error", "data": json.dumps({"code": "internal", "msg": "服务异常,请稍后再试"})}
                return

            yield {"event": "done", "data": "{}"}
        finally:
            if acquired:
                session_sem.release()

    return EventSourceResponse(event_stream())
