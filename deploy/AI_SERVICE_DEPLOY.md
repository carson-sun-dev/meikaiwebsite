# AI 客服上线部署 SOP

> 目标:把 `ai-service` + `qdrant` 接入既有的 `deploy/docker-compose.prod.yml` 栈,完成网站 AI 客服上线。
> 假设:服务器已按 `TENCENT_CLOUD.md` 跑过 backend + web + nginx + certbot,HTTPS 工作正常。

---

## 0. 内存预算(2C / 2G 机型)

| Service | mem_limit | 说明 |
|---|---|---|
| mysql | 600M | innodb_buffer_pool=256M + overhead |
| backend | 256M | Node.js |
| web | 80M | nginx static |
| nginx-proxy | 80M | edge nginx |
| **ai-service** | **500M** | FastAPI + LangGraph(去 PaddleOCR 后) |
| **qdrant** | **400M** | 向量库 + BM25 全文 |
| **合计** | **~1.92G** | 留 ~80M 系统余量;OOM 优先级:ai-service 比 mysql 先死 |

如果服务器是 4G 内存可直接放宽到默认值。

---

## 1. 上线前 checklist

### 1.1 第三方 API Key

部署前在火山方舟 / 百度智能云 / LangFuse 后台先把以下 Key 申请好:

- [ ] **火山方舟**(必需):https://www.volcengine.com/product/ark
  - `DOUBAO_API_KEY` — Ark 控制台 → API Key 管理
  - `DOUBAO_LITE_ENDPOINT` — Ark 「在线推理」→ 创建 Doubao-Lite-32k 接入点 → 复制 ep-xxxxx
  - `DEEPSEEK_ENDPOINT` — 同上,创建 DeepSeek-V3.2 接入点
  - `DOUBAO_EMBEDDING_ENDPOINT` — 同上,创建 Doubao-Embedding 接入点
  - `DOUBAO_VISION_ENDPOINT` — 同上,创建 Doubao-Vision 接入点(Sprint 2 OCR 兜底用,可暂不填)
  - `VOLC_RERANKER_API_KEY` — 一般同 DOUBAO_API_KEY(同一 Ark 入口)
- [ ] **百度 OCR**(可选 — 不开 CAD/图纸上传可跳):https://ai.baidu.com/tech/ocr_general
  - `BAIDU_OCR_API_KEY` / `BAIDU_OCR_SECRET_KEY`
- [ ] **LangFuse Cloud**(可选,观测用):https://cloud.langfuse.com
  - `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`
- [ ] **Qdrant**:自定义一段强密码作为 `QDRANT_API_KEY`(无需外部账号)

### 1.2 本地准备 Qdrant 知识源

服务器没有客户报价数据(`.gitignore` 屏蔽),需要本地把以下文件用 `scp` 传到服务器:

| 本地路径 | 服务器路径 | 用途 |
|---|---|---|
| `ai-service/data/projects_labeled.jsonl` | `~/meikai_website/ai-service/data/` | RAG 灌索引源数据 |
| `ai-service/data/quote_stats.json` | 同上 | Guardrail 输出侧 P10-P90 校验阈值 |
| `ai-service/data/quote_stats_per_sqm.json` | 同上 | 同上 |
| `ai-service/data/space_ratios.json` | 同上 | 空间×工艺占比锚定 |
| `ai-service/knowledge/manual_areas.json` | `~/meikai_website/ai-service/knowledge/` | 项目面积人工补全 |
| `ai-service/knowledge/manual_overrides.json` | 同上 | 业态/金额人工修正 |

---

## 2. 部署 5 步

> 假设服务器代码已 `git pull` 到最新 main。本地准备好上面的客户数据文件。

### 步骤 1 — 服务器上准备 `.env`

```bash
ssh meikai-prod
cd ~/meikai_website/ai-service
cp .env.prod.example .env
vi .env  # 填入 §1.1 全部 Key
```

`LLM_MODE` 务必设为 `live`(`.env.prod.example` 默认就是 live,但 docker-compose 显式兜底为 `mock` 防漏配,见 `prod.yml` 注释)。

同时在仓库根 `~/meikai_website/` 准备 `.env`(供 prod compose 用):

```bash
cd ~/meikai_website
cat > .env <<'EOF'
MYSQL_ROOT_PASSWORD=<强密码>
MYSQL_PASSWORD=<与 ai-service/.env 的 MYSQL_PASSWORD 一致>
MYSQL_DATABASE=meikai
MYSQL_USER=meikai
CORS_ORIGINS=https://www.meikaizs.com,https://meikaizs.com
VITE_SITE_ORIGIN=https://www.meikaizs.com
QDRANT_API_KEY=<与 ai-service/.env 一致>
LLM_MODE=live
EOF
```

⚠️ **两个 `.env` 的 `MYSQL_PASSWORD` 与 `QDRANT_API_KEY` 必须严格一致**,否则 ai-service 连不上 mysql / qdrant。

### 步骤 2 — scp 客户数据 + build 镜像

本地终端:
```bash
cd /Users/carrrson/developer/meikai_website
scp ai-service/data/projects_labeled.jsonl \
    ai-service/data/quote_stats.json \
    ai-service/data/quote_stats_per_sqm.json \
    ai-service/data/space_ratios.json \
    meikai-prod:~/meikai_website/ai-service/data/
scp ai-service/knowledge/manual_areas.json \
    ai-service/knowledge/manual_overrides.json \
    meikai-prod:~/meikai_website/ai-service/knowledge/
```

服务器:
```bash
cd ~/meikai_website
docker compose -f deploy/docker-compose.prod.yml build ai-service
# 首次约 5-8 分钟(下 python:3.12-slim + pip install)
```

### 步骤 3 — 启动 mysql / qdrant 并灌 Qdrant 索引

```bash
docker compose -f deploy/docker-compose.prod.yml up -d mysql qdrant
# 等 mysql healthy(约 30s)
docker compose -f deploy/docker-compose.prod.yml ps mysql  # STATUS 含 (healthy)

# 灌 Qdrant 一次性 job(用刚 build 好的 ai-service 镜像跑 ETL)
docker compose -f deploy/docker-compose.prod.yml run --rm \
  --entrypoint "" ai-service \
  python -m etl.build_index
```

`build_index.py` 会:
1. 读 `data/projects_labeled.jsonl`(line item 级)
2. 用 Doubao Embedding 向量化 + Jieba 分词建 BM25
3. 写入 Qdrant `quote_items_bge` collection

成功标志:`collection 'quote_items_bge' upserted N points`(N 应在百级)。

### 步骤 4 — 启动 ai-service + 重启 backend

```bash
docker compose -f deploy/docker-compose.prod.yml up -d backend ai-service
# backend 启动时会自动跑 migrate.ts → 建 ai_sessions / ai_checkpoints / ai_feedback 三表
# ai-service 启动时 langgraph saver.setup() 自动建 checkpoints/blobs/writes/migrations 四表

# 验证 healthcheck
sleep 30
docker compose -f deploy/docker-compose.prod.yml ps
# ai-service 应显示 (healthy)
docker logs meikai-ai-service-1 --tail 50  # 应见 "graph compiled with checkpointer=AIOMySQLSaver"
```

如果日志显示 `降级 InMemorySaver`,说明 mysql 连不通(密码不对 / 网络隔离),先排查再继续。

### 步骤 5 — 切换 nginx + 重启 web + 验证

```bash
# 1. 切边缘 nginx 到 ssl 配置(若尚未切)
cp deploy/edge.ssl.conf deploy/edge.active.conf

# 2. 启 web + nginx-proxy
docker compose -f deploy/docker-compose.prod.yml up -d web nginx-proxy

# 3. reload nginx 让新 SSE 路由生效
docker compose -f deploy/docker-compose.prod.yml exec nginx-proxy nginx -t
docker compose -f deploy/docker-compose.prod.yml exec nginx-proxy nginx -s reload

# 4. 验证 /api/ai/chat SSE
curl -N -X POST https://www.meikaizs.com/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"想开个火锅店,装修要多少钱"}' --max-time 30
# 预期看到 event: meta / delta / done 流式输出
```

5. **打开 https://www.meikaizs.com,右下角应有 💬 悬浮按钮 → 点开 ChatWidget,试两轮对话验证 multi-turn**:
   - 第一轮:"想开个火锅店,装修要多少钱" → 应识别 storefront
   - 第二轮:"200 平米" → 应直接出报价,不再问业态

---

## 3. 常见踩坑

### 3.1 ai-service 启动日志见 `降级 InMemorySaver`

原因:aiomysql 连不上 mysql。最常见是:
1. **mysql_data 卷密码漂移**:`mysql_data` 是旧容器留下的,卷内密码 ≠ 当前 `.env`。处理:
   ```bash
   docker compose -f deploy/docker-compose.prod.yml down
   docker volume rm meikai_mysql_data  # ⚠️ 会丢库内数据,首次部署可接受
   docker compose -f deploy/docker-compose.prod.yml up -d mysql
   ```
2. **缺 cryptography**:已在 `pyproject.toml` 修复;若 build 时间老于 2026-06-19,需 rebuild ai-service 镜像。
3. **mysql 还没 healthy 就启 ai-service**:`depends_on: service_healthy` 已挡;手动 up 时先单独起 mysql 等 30s 再起 ai-service。

### 3.2 `/api/ai/chat` 返回 502 或挂住

- nginx 配置必须 `proxy_buffering off`(`edge.ssl.conf` 已设);若改过本地副本检查这一行。
- ai-service healthcheck 是否通过:`docker compose ps ai-service` 看到 `(healthy)`。
- 看 ai-service 日志:`docker logs meikai-ai-service-1 -f`。

### 3.3 Qdrant 灌索引失败

- 检查 `QDRANT_API_KEY` 在两个 `.env` 是否一致。
- 检查 `ai-service/data/projects_labeled.jsonl` 是否真的传到位:
  `docker compose run --rm --entrypoint sh ai-service -c 'ls -la data/'`
- 检查 Doubao Embedding endpoint 是否正确:在 Ark 控制台测试该 ep。

### 3.4 LangFuse 连不上

如果不需要观测,把 `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` 留空即可,ai-service 不会因此崩(代码侧没硬依赖)。需要观测时填 Cloud 的 key,在 LangFuse Web 即可看 trace。

### 3.5 ai-service OOM 被杀

- 看 `dmesg | grep -i oom` 或 `docker events`。
- ai-service `mem_limit: 500m` 是按"去 PaddleOCR + 远程 Provider"测算的;若不慎装了 `[local]` extras 会暴涨,务必保持 prod 不装。
- LLM 上下文如果接近 32k 也可能瞬时撑爆,DESIGN §11.1 有 `memory_degrade_mb=400` 触发降级,实测中观察。

---

## 4. 回滚

如果上线后发现问题,临时关掉 AI 客服:

```bash
# 选项 A:停 ai-service,前端 ChatWidget 调 /api/ai/chat 会失败但站点其他功能不受影响
docker compose -f deploy/docker-compose.prod.yml stop ai-service qdrant

# 选项 B:nginx 层屏蔽,前端拿 502/404,可用维护页代替(改 edge.active.conf 把 /api/ai/ 改 return 503)
# 然后 nginx -s reload
```

数据库改动是幂等只增的(`CREATE TABLE IF NOT EXISTS`),无需回滚 schema。
