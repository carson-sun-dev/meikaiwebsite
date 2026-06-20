# meikai ai-service

美恺装饰 AI 客服与智能报价系统。本仓库为 public 仓库,设计文档 (`DESIGN.md`) 与会话记录 (`WORKLOG_*.md`) 不入库,本地保留;部署文档见 [`deploy/AI_SERVICE_DEPLOY.md`](../deploy/AI_SERVICE_DEPLOY.md)。

## 架构概览

- **后端**:FastAPI + LangGraph + Hybrid RAG(Qdrant 服务端 BM25 + IDF)
- **LLM**:火山方舟(Doubao Lite / DeepSeek)统一入口,SSE 流式输出
- **持久化**:MySQL (langgraph-checkpoint-mysql) + Qdrant (向量+全文)
- **观测**:LangFuse trace(可选)
- **入口**:Nginx `/api/ai/*` → ai-service:8000

模块布局:

```
app/
  main.py               FastAPI 入口 + /healthz + /api/ai/chat(SSE) + lifespan
  config.py             Pydantic Settings(三 provider 抽象 + Guardrail 阈值)
  graphs/               LangGraph:router + subgraphs(报价/闲聊) + state
  guardrails/           输出侧 quote_sanity 校验
  infra/                LLM / embedding / reranker / ocr / qdrant / checkpointer 抽象
  tools/                quote(三业态报价) + rag(Hybrid 检索)
schemas/                Pydantic 三业态 slot 定义
knowledge/              人工词典 / persona / question_bank
```

## 部署上线

直接看 [`deploy/AI_SERVICE_DEPLOY.md`](../deploy/AI_SERVICE_DEPLOY.md)。简言之 5 步:

1. 服务器拉代码,复制 `.env.prod.example` → `.env` 填真 Key
2. `docker compose -f deploy/docker-compose.prod.yml build ai-service`
3. 灌 Qdrant 索引一次(`etl/build_index.py`)
4. `docker compose -f deploy/docker-compose.prod.yml up -d`
5. `nginx -s reload` + 验证 `/api/ai/chat` SSE

## API Key 安全提示

- 真实 Key **永远不要**进库;`apikey.txt` / `.env` 已在仓库根 `.gitignore`
- 生产 Key 仅在服务器 `.env` 现场填,经 docker-compose `env_file` 注入
- DESIGN.md / WORKLOG_*.md 含商业策略与报价数据,**不进 public 仓库**(.gitignore 已屏蔽)

## 与网站现有栈集成

详见 DESIGN §9(本地文档)。要点:

- Nginx `/api/ai/chat` 必须 `proxy_buffering off`,否则 SSE 不流出
- 复用网站 MySQL 库(新增 `ai_sessions` / `ai_checkpoints` / `ai_feedback` 三表,见 `backend/src/db/migrate.ts`)
- 转人工时 ai-service 内网调 `backend:3001/api/leads/quote` 复用现有留资链路

## 集成测试说明(本地补回归时参考)

> 本仓库默认不在 CI 跑 ai-service 测试(prod 上线路径)。
> 本地若要做回归,见下:

- **单测**:`python -m pytest -v`(60 项,零外部依赖,集成自动 deselect)
- **集成**:`python -m pytest -m integration -v`(需 docker mysql 可达,否则优雅 skip)
- **schema 注记**:`backend/src/db/migrate.ts` 的 `ai_checkpoints` 表是历史预留;
  实际 langgraph-checkpoint-mysql 3.0.0 `setup()` 自建 4 张表
  (`checkpoints` / `checkpoint_blobs` / `checkpoint_writes` / `checkpoint_migrations`)
- **mysql 密码同步**:若 `mysql_data` volume 是旧容器留下的,密码可能与当前 `.env` 不一致。
  fixture 检测 access denied 会 skip 并打印重建命令。
