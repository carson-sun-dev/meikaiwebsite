"""真 MySQL checkpointer 集成测试 — Sprint 2 Phase A。

跑法:
    docker compose up -d mysql       # 顶层目录
    pytest -m integration -v          # 默认套件会跳过这些

WHY 单独切 integration 文件而非塞进 test_multi_turn.py:
- test_multi_turn 跑 InMemorySaver,零外部依赖,被默认套件秒过
- 集成测试有 docker 依赖,在物理位置上隔离 → tests/integration/ 子目录提示读者
  "这些是要起服务才能跑的"

WHY 复用 test_multi_turn.py 的 Stub LLMs(import 而不复制):
- 测试输入/L2 行为与单测一致,保持"逻辑路径相同,只换 saver"的对照原则
- 集成测试聚焦验证持久化,不验业务逻辑细节(已被单测覆盖)
"""
from __future__ import annotations

import pytest

from app.graphs import build_graph
from app.graphs import router as router_mod
from app.graphs import slots as slots_mod
from app.graphs import subgraphs as sg_mod
from app.infra.checkpointer import open_checkpointer

# 复用单测里的 Stub LLM(意图见模块 docstring)
from tests.test_multi_turn import (
    PromptEchoLLM,
    QuoteBlockEchoLLM,
    StubLLM,
    _collect_deltas,
)


# WHY autouse stub RAG:集成测试聚焦 checkpointer,RAG 走真 Qdrant 会引第二个 docker 依赖
@pytest.fixture(autouse=True)
def _stub_rag(monkeypatch):
    async def _empty(**_kw):
        return []
    monkeypatch.setattr(sg_mod, "retrieve_quote_examples", _empty)


@pytest.fixture
def patch_llms(monkeypatch):
    def _patch(slots_llm, subgraph_llm, router_llm):
        monkeypatch.setattr(slots_mod, "get_llm_client", lambda: slots_llm)
        monkeypatch.setattr(sg_mod, "get_llm_client", lambda: subgraph_llm)
        monkeypatch.setattr(router_mod, "get_llm_client", lambda: router_llm)
    return _patch


# ---- 测试用例 ----

@pytest.mark.integration
async def test_saver_creates_langgraph_tables(mysql_saver, mysql_test_config):
    """断言 AIOMySQLSaver.setup() 实际建的是 langgraph 自带 schema 的 4 张表。

    WHY 显式断言四张表名:
    - backend/migrate.ts 里手建的 `ai_checkpoints` 表(session_id/thread_ts/state_json)
      其实没被 langgraph 使用 — 这条测试把"我们用的是 langgraph 自带 schema"变成可见事实
    - 防止以后有人误以为可以删 langgraph 这套表去用 ai_checkpoints,导致跨进程持久化挂掉
    """
    import aiomysql

    cfg = mysql_test_config
    conn = await aiomysql.connect(
        host=cfg["host"], port=cfg["port"],
        user=cfg["user"], password=cfg["password"],
        db=cfg["db"], autocommit=True,
    )
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = %s",
                (cfg["db"],),
            )
            rows = await cur.fetchall()
    finally:
        conn.close()

    table_names = {r[0].lower() for r in rows}
    expected = {"checkpoints", "checkpoint_blobs", "checkpoint_writes", "checkpoint_migrations"}
    missing = expected - table_names
    assert not missing, f"langgraph schema 缺表:{missing};实际:{table_names}"
    # WHY 不检查 ai_checkpoints 不存在:本测试与 backend/migrate.ts 共享 meikai 库,
    #     ai_checkpoints 是后端建的(不被 langgraph 用),可能存在 — 它的存在不影响测试结论:
    #     "langgraph 用自己的 4 张表"。把"backend 那张表没被用"留给 README 文档说明
    log_msg = f"langgraph 4 张表已建于 meikai 库;库内现有表:{sorted(table_names)}"
    print(log_msg)  # noqa: T201 — pytest -s 时可见 schema 全貌


@pytest.mark.integration
async def test_state_persists_across_graph_instances(mysql_saver, patch_llms):
    """跨 graph 实例(模拟进程重启)+ 同 thread_id → state 仍可见。

    WHY 这是 MySQL 持久化最核心的价值断言:
    - 单测用 InMemorySaver 看的是"同进程跨轮",而生产里 uvicorn worker 可能重启
    - 这里 build_graph 两次拿到两个 CompiledGraph 实例(等价于两个进程),共享同一 saver
    - 通过则证明 state 真落盘了 MySQL,不是内存里残留
    """
    # ---- 轮 1:用 graph1,产生 state + 落盘 ----
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": "火锅店"}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    graph1 = build_graph(checkpointer=mysql_saver)
    config = {"configurable": {"thread_id": "cross-instance-A"}}

    turn1, _ = await _collect_deltas(
        graph1, {"user_msg": "想开个火锅店,装修要多少钱"}, config,
    )
    assert "quote_block" not in turn1, "轮 1 应走引导分支"
    assert "已知信息" in turn1
    assert "火锅店" in turn1

    # ---- 模拟进程重启:**新** graph 实例,但共享同一 saver(MySQL 已落盘) ----
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": null}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    graph2 = build_graph(checkpointer=mysql_saver)
    assert graph2 is not graph1, "fixture 应给出不同实例(模拟重启)"

    turn2, _ = await _collect_deltas(
        graph2, {"user_msg": "200 平米"}, config,
    )

    # 关键断言:轮 2 命中报价分支 = 上一轮 state(business_type=火锅店、is_quote_intent=True)
    # 被 MySQL 持久化并由新 graph 实例读出
    assert "基础档" in turn2, f"跨实例同 thread 应继承槽位,得到:\n{turn2[:300]}"
    assert "中端档" in turn2
    assert "高端档" in turn2
    assert "200㎡" in turn2
    assert "火锅店" in turn2
    assert "这只是AI输出的价格" in turn2


@pytest.mark.integration
async def test_thread_isolation_in_mysql(mysql_saver, patch_llms):
    """同一 saver 下,thread A 的 state 不应漏到 thread B。"""
    # thread A:报价齐套
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": 200, "business_type": "火锅店"}'),
        subgraph_llm=QuoteBlockEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    graph = build_graph(checkpointer=mysql_saver)
    turn_a, _ = await _collect_deltas(
        graph, {"user_msg": "我开火锅店 200 平 多少钱"},
        {"configurable": {"thread_id": "iso-A"}},
    )
    assert "基础档" in turn_a

    # thread B:全新会话,slots LLM 模拟"抽不到任何字段"
    patch_llms(
        slots_llm=StubLLM('{"is_quote_intent": true, "area_sqm": null, "business_type": null}'),
        subgraph_llm=PromptEchoLLM(),
        router_llm=StubLLM("storefront"),
    )
    turn_b, _ = await _collect_deltas(
        graph, {"user_msg": "想咨询价格"},
        {"configurable": {"thread_id": "iso-B"}},
    )

    assert "基础档" not in turn_b, "thread B 不应继承 thread A 的槽位"
    assert "quote_block" not in turn_b
    assert "已知信息" in turn_b


@pytest.mark.integration
async def test_open_checkpointer_factory_returns_mysql_when_reachable(monkeypatch, mysql_test_config):
    """覆盖 open_checkpointer() 工厂的"成功路径" — MySQL 可达时应返回 AIOMySQLSaver。

    WHY:降级路径(MySQL 挂)在 mock E2E 已验,成功路径只在生产实际启动时才走;
        这里把 settings 临时指向测试 MySQL,显式覆盖成功分支
    """
    from langgraph.checkpoint.mysql.aio import AIOMySQLSaver

    from app import config as cfg_mod
    cfg = mysql_test_config

    # WHY 改 Settings 而非传参:open_checkpointer 是无参 ctx mgr,依赖 get_settings();
    #     monkeypatch 覆盖 settings 对象的字段是最干净的做法
    settings = cfg_mod.get_settings()
    monkeypatch.setattr(settings, "mysql_host", cfg["host"])
    monkeypatch.setattr(settings, "mysql_port", cfg["port"])
    monkeypatch.setattr(settings, "mysql_user", cfg["user"])
    monkeypatch.setattr(settings, "mysql_password", cfg["password"])
    monkeypatch.setattr(settings, "mysql_db", cfg["db"])

    async with open_checkpointer() as saver:
        assert isinstance(saver, AIOMySQLSaver), \
            f"MySQL 可达时工厂应返回 AIOMySQLSaver,得到 {type(saver).__name__}"
