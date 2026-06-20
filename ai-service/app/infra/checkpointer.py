"""LangGraph Checkpointer 工厂 — Sprint 2 step 6:多轮对话状态持久化。

DESIGN 锚点:
- §3 Sprint 2 step 6:MySQL checkpointer + thread_id 跨轮 state 复用(用户不必重复说面积)
- §11.4 工程纪律:外部依赖不可达时降级,不阻断服务启动

WHY 主路径 MySQL,降级 InMemorySaver(而非崩):
- 简历级项目:MySQL 持久化体现"生产就绪",mock/dev 环境没起 mysql 时仍能跑
- 严格要求 MySQL = 提高新人/CI 起步门槛;静默降级 + WARN 日志 = 故障感知前提下保留体验
- 生产侧若 mysql 真挂应触发告警(后期接 langfuse alerts),不在本层硬挡

WHY 用 async ctx mgr 而非全局单例:
- AIOMySQLSaver.from_conn_string 自身是 async ctx mgr(管理 aiomysql 连接生命周期)
- 在 FastAPI lifespan 里 enter/exit 才能让连接随服务起停;放全局 lru_cache 会泄漏 conn
- 测试侧也可用 ctx mgr 包裹独立连接,不与生产单例耦合
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from app.config import get_settings

log = logging.getLogger("infra.checkpointer")


def _build_mysql_conn_string() -> str:
    """从 Settings 拼 aiomysql 连接串。

    langgraph-checkpoint-mysql 的 AIOMySQLSaver.parse_conn_string 走标准 URL 解析,
    所以这里只需 mysql://user:password@host:port/db(scheme 名实际被忽略,但保留语义)
    """
    s = get_settings()
    user = s.mysql_user or "root"
    pw = s.mysql_password or ""
    auth = f"{user}:{pw}@" if pw else f"{user}@"
    return f"mysql://{auth}{s.mysql_host}:{s.mysql_port}/{s.mysql_db}"


@asynccontextmanager
async def open_checkpointer() -> AsyncIterator[BaseCheckpointSaver]:
    """获取 LangGraph 兼容的 checkpointer。

    主路径:AIOMySQLSaver(连接 mysql_host)
    降级:InMemorySaver(MySQL 不可达 / 缺依赖)

    用法:
        async with open_checkpointer() as saver:
            graph = build_graph(saver)
            ...

    WHY 把降级写在工厂里而非让调用方判断:
    - 启动时统一一处处理"用什么 saver",业务代码拿到的是 BaseCheckpointSaver 协议,
      不需要知道底层是 mysql 还是 in-memory
    - InMemorySaver 也实现 BaseCheckpointSaver,protocol-level 完全兼容
    """
    conn_string = _build_mysql_conn_string()
    log.info("attempting MySQL checkpointer: %s", _redact(conn_string))

    try:
        # WHY 延迟 import:让本模块在缺 aiomysql 时仍可 import(测试场景纯走 in-memory)
        from langgraph.checkpoint.mysql.aio import AIOMySQLSaver
    except ImportError as e:
        log.warning("langgraph-checkpoint-mysql 未安装,降级 InMemorySaver:%s", e)
        yield InMemorySaver()
        return

    try:
        async with AIOMySQLSaver.from_conn_string(conn_string) as saver:
            # WHY setup() 必须显式调用:官方文档要求首次使用前建表(checkpoints /
            #     checkpoint_blobs / checkpoint_writes / checkpoint_migrations 四张),
            #     幂等可重复调,二次启动会 no-op
            await saver.setup()
            log.info("MySQL checkpointer ready")
            yield saver
    except Exception as e:
        # WHY catch-all:aiomysql 连接异常、权限、表创建失败都该回落,不阻断启动
        log.warning(
            "MySQL checkpointer init failed (%s),降级 InMemorySaver — "
            "槽位/路由会跨进程丢失,生产环境请排查 MySQL 连通性",
            e,
        )
        yield InMemorySaver()


def _redact(conn_string: str) -> str:
    """日志安全:把连接串里的密码段隐去。"""
    if "@" not in conn_string or "//" not in conn_string:
        return conn_string
    scheme, rest = conn_string.split("//", 1)
    if "@" not in rest:
        return conn_string
    auth, tail = rest.split("@", 1)
    if ":" in auth:
        user = auth.split(":", 1)[0]
        return f"{scheme}//{user}:***@{tail}"
    return conn_string
