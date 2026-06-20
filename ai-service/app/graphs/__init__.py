"""LangGraph 编排入口 — Sprint 2 step 6:multi-turn 接 checkpointer。

```
        START
          │
          ▼
      ┌────────┐
      │ router │  ← L0 LLM 业态分类(写 state.business_line)
      └────────┘   ※ state.business_line 已存在则短路跳过 LLM(step 6)
          │ conditional_edge(route_to_subgraph)
   ┌──────┼───────┐
   ▼      ▼       ▼
storefront office residential   ← stream_writer 推 L2 token
   │      │       │              ※ 入口 merge 上一轮 slots(monotonic)
   └──────┼───────┘
          ▼
         END  ← checkpointer 持久化 state 到 thread_id 名下,下一轮接续读出
```

WHY Sprint 2 step 1 的 lru_cache 在 step 6 移除:
- checkpointer 是运行期资源(MySQL 连接生命周期与 lifespan 绑定),不能在 import 时就编译完
- build_graph(checkpointer) 由 FastAPI lifespan 调用,产物存 app.state.graph
- 测试侧用 build_graph(InMemorySaver()) 拿独立实例,不污染生产单例
"""
from __future__ import annotations

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph

from app.graphs.router import classify_node, route_to_subgraph
from app.graphs.state import ChatState
from app.graphs.subgraphs import office_node, residential_node, storefront_node


def build_graph(checkpointer: BaseCheckpointSaver | None = None):
    """编译 LangGraph;可选传 checkpointer 实现跨轮状态持久化。

    WHY 允许 checkpointer=None:
    - 单测中部分场景(如 router 行为)不需要状态持久化,None 等价于"一次性图"
    - 生产/multi-turn 测试要传 saver 才能让 state.slots 跨轮可见
    """
    g = StateGraph(ChatState)
    g.add_node("router", classify_node)
    g.add_node("storefront", storefront_node)
    g.add_node("office", office_node)
    g.add_node("residential", residential_node)

    g.add_edge(START, "router")
    g.add_conditional_edges(
        "router",
        route_to_subgraph,
        # WHY 显式 mapping 而非裸 dispatch:让图的可达性在编译期可校验,
        #     SubGraph 增减时漏配会立即 ValueError 而非运行时找不到节点
        {
            "storefront": "storefront",
            "office": "office",
            "residential": "residential",
        },
    )
    g.add_edge("storefront", END)
    g.add_edge("office", END)
    g.add_edge("residential", END)

    return g.compile(checkpointer=checkpointer) if checkpointer else g.compile()


# WHY 兼容旧调用(get_graph):Sprint 2 step 1 留下的入口,test_subgraphs_quote.py 仍在用。
#     无 checkpointer 等价于 step 1 的行为 — 保持兼容直到测试全切到 build_graph
def get_graph():
    return build_graph(checkpointer=None)
