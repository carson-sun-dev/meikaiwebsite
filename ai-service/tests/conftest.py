"""pytest 共享 fixtures — Sprint 2 Phase A 集成测试入口。

DESIGN 锚点:
- §13.1 LangGraph checkpointer 持久化:本地 docker mysql 真路径要在集成测试里验
- §11.4 工程纪律:集成测试 fixture 必须能在 MySQL 缺席时 skip 而非 fail

WHY 集成测试默认跳过(pyproject.toml addopts="-m 'not integration'"):
- 单测应秒过零依赖;集成测试需 `docker compose up -d mysql`,作为显式动作触发
- CI 短期内只跑单测;集成测试本地手跑或后续 CI 加 docker service 时再纳管

WHY 这个 conftest 同时管 marker 与 fixture:
- pytest 找 conftest 是按目录上溯;放 tests/ 让所有 integration test 共享 mysql_saver
- 单测(默认套件)不会调 mysql_saver,fixture 是 lazy 的,集成跳过时零成本
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import AsyncIterator

import pytest
import pytest_asyncio


# WHY 自动加载顶层 .env:本仓库 docker compose 启动 mysql 时读 /meikai_website/.env 的
#     MYSQL_ROOT_PASSWORD 配置 root 密码;让测试自动对齐这套配置,开发者不必再设环境变量
def _load_repo_dotenv() -> dict[str, str]:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return {}
    out: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_REPO_ENV = _load_repo_dotenv()


def _resolved_mysql_config() -> dict[str, str | int]:
    """集成测试连接 MySQL 的配置 — process env > 顶层 .env > 硬编码 default。

    WHY 用 meikai 账户 + 现有 meikai 库而非 root + 独立测试库:
    - mysql:8.0 镜像默认 root@'localhost'(socket only),从 host 通过 127.0.0.1 走 TCP
      会被 root@'%' 拒(权限上 root 只允许容器内 socket)
    - 改 docker-compose 加 MYSQL_ROOT_HOST=% 会暴露生产 root 远程入口,不可取
    - meikai 用户在 docker entrypoint 自动创建时是 `'meikai'@'%'`,已有 meikai 库全部权限
    - 代价:测试 langgraph 4 张表 (checkpoints / checkpoint_blobs / checkpoint_writes /
      checkpoint_migrations) 共享 meikai 库与开发数据共存;fixture 在 session 前后 drop 这
      四张表清场,与 backend/migrate.ts 建的 submissions/ai_sessions/ai_feedback 共存
    """
    return {
        "host": os.getenv("TEST_MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("TEST_MYSQL_PORT", "3306")),
        "user": os.getenv(
            "TEST_MYSQL_USER",
            _REPO_ENV.get("MYSQL_USER", "meikai"),
        ),
        "password": os.getenv(
            "TEST_MYSQL_PASSWORD",
            _REPO_ENV.get("MYSQL_PASSWORD", "meikai_pass_change_me"),
        ),
        "db": os.getenv(
            "TEST_MYSQL_DB",
            _REPO_ENV.get("MYSQL_DATABASE", "meikai"),
        ),
    }


# WHY 模块常量:langgraph-checkpoint-mysql 3.0.0 setup() 实际建的 4 张表(详见
#     .venv/.../langgraph/checkpoint/mysql/base.py:MIGRATIONS)。改包版本前别动这个清单
_LANGGRAPH_CHECKPOINT_TABLES = (
    "checkpoint_writes",
    "checkpoint_blobs",
    "checkpoints",
    "checkpoint_migrations",
)


async def _mysql_ping(cfg: dict) -> bool:
    """探测 MySQL 是否可达 — 失败立即返 False,不抛。"""
    try:
        import aiomysql

        conn = await asyncio.wait_for(
            aiomysql.connect(
                host=cfg["host"], port=cfg["port"],
                user=cfg["user"], password=cfg["password"],
                db=cfg["db"], autocommit=True,
            ),
            timeout=2.0,
        )
    except Exception:
        return False
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
        return True
    finally:
        conn.close()


async def _drop_langgraph_tables(cfg: dict) -> None:
    """清场:drop langgraph 自管理的 4 张表,与 backend/migrate.ts 的表共存不冲突。"""
    import aiomysql
    conn = await aiomysql.connect(
        host=cfg["host"], port=cfg["port"],
        user=cfg["user"], password=cfg["password"],
        db=cfg["db"], autocommit=True,
    )
    try:
        async with conn.cursor() as cur:
            # WHY 关 FK check + drop 顺序无关:langgraph 自带表互相不依赖,但保险
            await cur.execute("SET FOREIGN_KEY_CHECKS=0")
            for t in _LANGGRAPH_CHECKPOINT_TABLES:
                await cur.execute(f"DROP TABLE IF EXISTS `{t}`")
            await cur.execute("SET FOREIGN_KEY_CHECKS=1")
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def _skip_integration_if_mysql_down(request):
    """带 @pytest.mark.integration 的测试:MySQL 不可达直接 skip(开发者忘起 docker 时友好)。

    WHY autouse + 仅作用于 integration 标记的测试:
    - autouse 让集成测试不必每条都写 skipif,降低样板
    - 用 request.node.get_closest_marker 判断,单测零开销(不带 marker 直接 return)
    """
    if request.node.get_closest_marker("integration") is None:
        return
    cfg = _resolved_mysql_config()
    ok = asyncio.run(_mysql_ping(cfg))
    if not ok:
        pytest.skip(
            f"MySQL 不可达 ({cfg['host']}:{cfg['port']} as {cfg['user']}) — "
            f"跑集成测试前请先 `docker compose up -d mysql`(顶层目录),"
            f"或导出 TEST_MYSQL_PASSWORD"
        )


@pytest_asyncio.fixture(scope="session")
async def mysql_saver() -> AsyncIterator:
    """session-scope MySQL checkpointer fixture — 清场 → setup → yield → 清场。

    WHY ping 失败时 skip 而非 error:
    - autouse 的 _skip_integration_if_mysql_down 只检查 ping,fixture 内部仍可能因为
      meikai 账号密码不对(mysql_data 卷里的密码与 .env 不同步)而失败
    - fixture 内 try/except 转 pytest.skip 让用户看到清晰的 skip 原因,而非红色 ERROR 栈

    WHY session scope:
    - AIOMySQLSaver.setup() 建 4 张表 + 一次连接握手 ~500ms,session 共享让多个集成
      测试只付一次代价
    - 测试之间通过不同 thread_id 隔离 state,不必每个测试新库

    WHY 在现有 meikai 库内,而非独立测试库:
    - 见 _resolved_mysql_config 注释:mysql 8.0 默认 root 不让远程连;meikai 用户没
      CREATE DATABASE 权限,只能在已有库里折腾
    - 与 backend/migrate.ts 的 submissions/ai_sessions/ai_feedback 等表共存(命名空间不冲突)
    - 前后清场只 drop langgraph 自管理的 4 张表,不动开发数据
    """
    from langgraph.checkpoint.mysql.aio import AIOMySQLSaver

    cfg = _resolved_mysql_config()

    # 0. 二次验证 — autouse ping 通了不代表 meikai 账号可用(密码可能与 mysql_data 卷不同步)
    if not await _mysql_ping(cfg):
        pytest.skip(
            f"MySQL meikai 账号不可用 ({cfg['user']}@{cfg['host']}) — "
            f"通常是 mysql_data 卷里旧密码 ≠ 当前 .env;"
            f"重建容器:`docker compose down && docker volume rm meikai_website_mysql_data && "
            f"docker compose up -d mysql`,或显式 export TEST_MYSQL_PASSWORD"
        )

    # 1. 前置清场:drop 上次跑剩的 langgraph 表(若有)
    await _drop_langgraph_tables(cfg)

    # 2. 拼 saver 连接串 + setup 建 langgraph 4 张表
    conn_string = (
        f"mysql://{cfg['user']}:{cfg['password']}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['db']}"
    )
    async with AIOMySQLSaver.from_conn_string(conn_string) as saver:
        await saver.setup()
        try:
            yield saver
        finally:
            pass  # AIOMySQLSaver 自管理 connection,ctx 退出会清

    # 3. session 退出 → 再次清场,本地下次跑零残留
    await _drop_langgraph_tables(cfg)


@pytest.fixture(scope="session")
def mysql_test_config() -> dict[str, str | int]:
    """暴露解析后的连接配置给测试体内使用(如直接 SELECT 验表结构)。"""
    return _resolved_mysql_config()
