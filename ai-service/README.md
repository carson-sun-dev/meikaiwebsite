# meikai ai-service

美恺装饰 AI 客服与智能报价系统。完整设计见 [DESIGN.md](./DESIGN.md);评审过程见 [SESSION_2026-05-30.md](./SESSION_2026-05-30.md)。

## 状态(2026-06-07)

Sprint 1 进行中。已就位:
- `pyproject.toml` / `Dockerfile` / `.env.full.example` / `.env.prod.example`
- `app/main.py` FastAPI 骨架 + `/healthz` + `/api/ai/chat` SSE(mock LLM)
- `app/config.py` Pydantic Settings(含三 provider 字段)
- `app/infra/{llm_client,embedding,reranker,ocr,qdrant_client}.py` Provider 抽象 + mock/local/api 多实现
- 目录骨架(schemas / knowledge / etl / data / logs / tests / guardrails)

待完成(Sprint 1 剩余):ETL 灌 Qdrant、Jieba 分词器 + 装修词典、MySQL migration、Guardrails 实现(§5.7)。

## 本地启动(开发模式)

```bash
# 1) Python 3.12(用 pyenv / uv 装)
pyenv install 3.12.7 && pyenv local 3.12.7

# 2) 装依赖(推荐 uv,fallback pip)
uv sync   # 或:python -m venv .venv && source .venv/bin/activate && pip install -e .

# 3) 配置(本地完整版用 full,生产 2C4G 用 prod)
cp .env.full.example .env
# 编辑 .env(Sprint 1/2 期间 LLM_MODE=mock 即可,不需要真 key)

# 4) 起服务
uvicorn app.main:app --reload --port 8000

# 5) 验证
curl http://localhost:8000/healthz
curl -N -X POST http://localhost:8000/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"我想开一家咖啡店"}'
```

## API Key 安全提示

- 真实 Key **永远不要**写进 `.env` 之外的文件;`apikey.txt` 已在仓库根 `.gitignore`
- 部署到生产时通过 docker-compose `env_file` 注入,不要 `ENV` 写死

## 与现网站点集成

参见 [DESIGN.md §9 网站接入计划](./DESIGN.md)。简言之:
- Nginx 加 `/api/ai/*` 转 `ai-service:8000`,SSE 必须 `proxy_buffering off`
- 复用现网 MySQL(新增三张表见 `backend/src/db/migrate.ts`)
- 转人工时内网调 `backend:3001/api/leads/quote`

## 测试

```bash
# 单测(零外部依赖,默认套件 — 集成测试自动排除)
python -m pytest -v

# 集成测试(需 docker mysql 起来 + 账号密码与当前 .env 同步)
docker compose up -d mysql            # 在仓库顶层目录
python -m pytest -m integration -v    # MySQL 不可达时优雅 skip

# 跑全部(单测 + 集成)
python -m pytest -m "integration or not integration" -v
```

### 集成测试说明

- **范围**:`tests/integration/test_mysql_checkpointer.py` 验证 LangGraph multi-turn 走真 MySQL
  (跨进程跨轮 state 持久化、thread 隔离、open_checkpointer 工厂成功路径)
- **schema 注记**:`backend/src/db/migrate.ts` 里的 `ai_checkpoints` 表是历史预留,
  **实际不被使用** — langgraph-checkpoint-mysql 3.0.0 `setup()` 自建 4 张表
  (`checkpoints` / `checkpoint_blobs` / `checkpoint_writes` / `checkpoint_migrations`)
- **测试库 = 现有 meikai 库**:fixture 在 session 前后只 drop langgraph 的 4 张表,
  不动 backend 建的 submissions/ai_sessions/ai_feedback;原因见 `tests/conftest.py:_resolved_mysql_config` 注释
- **mysql 密码同步问题**:若 `mysql_data` volume 是旧容器留下的,密码可能与当前 `.env`
  不一致。fixture 检测到 access denied 会自动 skip 并打印重建命令:
  ```bash
  docker compose down && docker volume rm meikai_website_mysql_data && docker compose up -d mysql
  ```
