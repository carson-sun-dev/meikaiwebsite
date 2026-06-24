# AI 客服上线部署 SOP

> 目标:把 `ai-service` + `qdrant` 接入既有的 `deploy/docker-compose.prod.yml` 栈。
> **流程:本地全栈预演 → 通过后 ssh 服务器走同样流程**。本地与服务器复用同一份 compose,只换 `.env` + nginx conf。

---

## 0.5 占位上线模式(2026-06-24 临时启用)

AI 客服仍在迭代,前端用 `ChatPanelPlaceholder.vue` 占位、后端 `ai-service` + `qdrant` 用
`profiles: [ai]` 默认不启,节省 ~900M 内存,2C2G 服务器只承担网站主体 4 个服务。

**部署命令** —— 不带 `--profile ai`,自然只起 mysql/backend/web/nginx-proxy:
```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env up -d
```

**恢复完整 AI 客服**(两步,均为单点改动):
1. 前端:`frontend/src/components/ChatWidget/ChatWidget.vue` 顶部 `import('./ChatPanelPlaceholder.vue')`
   改回 `import('./ChatPanel.vue')`,重新 `pnpm build`(或 docker compose build web)。
2. 后端:`docker compose ... --profile ai up -d`(本文 §4 步骤照常)。

期间 nginx 仍保留 `/api/ai/*` 路由,前端占位组件不发请求,无 502 风险;若有外部 curl 探测会
打到不存在的 upstream → 502,nginx 限流 zone 仍然生效。

---

## 0. 流程速览

```
阶段 B1 本地全栈预演(deploy/docker-compose.prod.yml + edge.local.conf)
   ↓ (浏览器 http://localhost 验 ChatWidget 通过)
阶段 B2 ssh 服务器(同 compose + edge.ssl.conf,只换 .env)
```

本地预演的意义:第一次跑 prod 镜像 + Qdrant 灌索引 + LangGraph 多轮 checkpointer + nginx SSE buffer 配置,任何一处错都不该在服务器现场调试。本地通过 = 服务器只剩 .env 与证书。

> ⚠️ 全文 `docker compose` 命令都必须带 `--env-file .env`(运行目录是仓库根)。
> 因为 `-f deploy/docker-compose.prod.yml` 让 compose 的 project dir 落到 `deploy/`,
> 默认只会读 `deploy/.env`(不存在),所以根 `.env` 必须显式指定。

---

## 1. 内存预算(2C / 2G 机型)

| Service | mem_limit | 说明 |
|---|---|---|
| mysql | 600M | innodb_buffer_pool=256M + overhead |
| backend | 256M | Node.js |
| web | 80M | nginx static |
| nginx-proxy | 80M | edge nginx |
| **ai-service** | **500M** | FastAPI + LangGraph(去 PaddleOCR 后) |
| **qdrant** | **400M** | 向量库 + BM25 全文 |
| **合计** | **~1.92G** | 留 ~80M 系统余量;OOM 优先级:ai-service 比 mysql 先死 |

本地 Mac 16G 内存可忽略 mem_limit;服务器 2G 机型必须遵守。

---

## 2. 上线前 checklist

### 2.1 第三方 API Key

部署前在以下平台申请好,本地预演 + 服务器都用同一份(同一组 Key):

- [ ] **火山方舟**(必需):https://www.volcengine.com/product/ark
  - `DOUBAO_API_KEY` — Ark 控制台 → API Key 管理
  - `DOUBAO_LITE_ENDPOINT` — Ark 「在线推理」→ 创建 Doubao-Lite-32k 接入点 → 复制 ep-xxxxx
  - `DEEPSEEK_ENDPOINT` — 同上,创建 DeepSeek-V3.2 接入点
  - `DOUBAO_EMBEDDING_ENDPOINT` — 同上,创建 Doubao-Embedding 接入点
  - `DOUBAO_VISION_ENDPOINT` — 同上(Sprint 2 OCR 兜底,可暂不填)
  - `VOLC_RERANKER_API_KEY` — 一般同 DOUBAO_API_KEY
- [ ] **百度 OCR**(可选 — 不开 CAD/图纸上传可跳):`BAIDU_OCR_API_KEY` / `BAIDU_OCR_SECRET_KEY`
- [ ] **LangFuse Cloud**(可选,观测用):`LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`
- [ ] **Qdrant**:自定义一段强密码作为 `QDRANT_API_KEY`(无需外部账号)

### 2.2 客户数据

| 路径 | 用途 | 本地 | 服务器 |
|---|---|---|---|
| `ai-service/data/quotes.jsonl` | RAG 灌索引源(line item 级,~3.2k 行) | ✓ 物理已有 | 需 scp |
| `ai-service/data/projects_labeled.jsonl` | RAG 业态过滤(项目级,line item 反查 business_line) | ✓ | 需 scp |
| `ai-service/data/quote_stats*.json` | Guardrail P10-P90 阈值 | ✓ | 需 scp |
| `ai-service/data/space_ratios.json` | 空间×工艺占比锚定 | ✓ | 需 scp |
| `ai-service/knowledge/manual_*.json` | 项目面积/金额人工修正 | ✓ | 需 scp |

`.gitignore` 屏蔽,代码库无,本地物理保留。本地预演无需任何动作;服务器步骤见 §4.2。

---

## 3. 配置差异(本地 vs 服务器)

部署步骤完全一样,只这五项不同:

| 项 | 本地 | 服务器 |
|---|---|---|
| Nginx conf | `cp edge.local.conf edge.active.conf`(80 端口,无 SSL) | `cp edge.ssl.conf edge.active.conf`(443 + Let's Encrypt) |
| `ai-service/.env` `ALLOWED_ORIGINS` | `http://localhost` | `https://www.meikaizs.com,https://meikaizs.com` |
| 仓库根 `.env` `CORS_ORIGINS` | `http://localhost` | `https://www.meikaizs.com` |
| 仓库根 `.env` `VITE_SITE_ORIGIN` | `http://localhost` | `https://www.meikaizs.com` |
| 旧 `mysql_data` 卷 | 本地 dev 期可能存在,需 `docker volume rm` 一次性清掉 | 全新机器,无 |

`LLM_MODE`、Key、QDRANT_API_KEY、MYSQL_PASSWORD 两侧用同一份。

---

## 4. 通用部署步骤(本地 + 服务器同源)

### 4.0 前置:准备两份 .env

**仓库根 `.env`**(给 docker compose 用):
```bash
cd /Users/carrrson/developer/meikai_website   # 本地;服务器是 ~/meikai_website
cat > .env <<'EOF'
MYSQL_ROOT_PASSWORD=<强密码>
MYSQL_PASSWORD=<同 ai-service/.env>
MYSQL_DATABASE=meikai
MYSQL_USER=meikai
CORS_ORIGINS=http://localhost                  # 服务器换 https://www.meikaizs.com
VITE_SITE_ORIGIN=http://localhost              # 服务器换 https://www.meikaizs.com
QDRANT_API_KEY=<同 ai-service/.env>
LLM_MODE=live
EOF
```

**`ai-service/.env`**(基于模板,填 Key):
```bash
cd ai-service
cp .env.prod.example .env
vi .env
# 填:DOUBAO_API_KEY / 4 endpoints / VOLC_RERANKER_API_KEY / BAIDU_OCR_API_KEY (可选)
#     QDRANT_API_KEY / MYSQL_PASSWORD / LANGFUSE_*(可选)
# 改:ALLOWED_ORIGINS=http://localhost  (服务器换 https://www.meikaizs.com,https://meikaizs.com)
```

⚠️ **MYSQL_PASSWORD / QDRANT_API_KEY 在两份 .env 必须严格一致**,否则 ai-service 连不上 mysql/qdrant。

### 4.1 [仅本地] 清旧 mysql 卷

本地 dev 期可能有旧 `mysql_data` 卷,密码与新 `.env` 不一致 → ai-service 会降级到 InMemorySaver。第一次预演前清掉:

```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env down
docker volume ls | grep mysql_data   # 看具体名,通常是 meikai_website_mysql_data
docker volume rm meikai_website_mysql_data
```

服务器是全新机型,跳过。

### 4.2 [仅服务器] scp 客户数据

本地预演已物理就绪,跳过。服务器:

```bash
# 本地执行
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

### 4.3 切 nginx active 配置 + build 镜像

```bash
cd /Users/carrrson/developer/meikai_website        # 本地;服务器是 ~/meikai_website

# 切 nginx active(本地用 local,服务器用 ssl)
cp deploy/edge.local.conf deploy/edge.active.conf  # 本地
# cp deploy/edge.ssl.conf  deploy/edge.active.conf  # 服务器

# build ai-service(首次约 5-8 min,本地 + 服务器都要 build 各自镜像)
docker compose -f deploy/docker-compose.prod.yml --env-file .env build ai-service
```

### 4.4 启 mysql / qdrant 并灌 Qdrant 索引

```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env up -d mysql qdrant

# 等 mysql healthy(约 30s),看到 STATUS 含 (healthy) 再继续
docker compose -f deploy/docker-compose.prod.yml --env-file .env ps mysql

# 灌索引(--rm 一次性 job,跑完即删)
docker compose -f deploy/docker-compose.prod.yml --env-file .env run --rm \
  --entrypoint "" ai-service \
  python -m etl.build_index
```

`build_index.py` 会:
1. 读 `data/quotes.jsonl`(line item 级,~3.2k 行,group header 行会被过滤)
2. Doubao Embedding 向量化 + Jieba 分词建 BM25
3. 写入 Qdrant `quote_items_bge` collection

成功标志:日志 `collection 'quote_items_bge' upserted N points`(百级)。

### 4.5 启 backend + ai-service

```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env up -d backend ai-service
# backend 启动会自动跑 migrate.ts → 建 ai_sessions / ai_checkpoints / ai_feedback 三表
# ai-service 启动 langgraph saver.setup() → 自建 checkpoints/blobs/writes/migrations 四表

sleep 30
docker compose -f deploy/docker-compose.prod.yml --env-file .env ps
# ai-service 应显示 (healthy)
docker compose -f deploy/docker-compose.prod.yml --env-file .env logs ai-service | tail -30
# 应见 "graph compiled with checkpointer=AIOMySQLSaver"
# 若见 "降级 InMemorySaver" → mysql 连不通,检查密码 / 卷
```

### 4.6 启 web + nginx-proxy

```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env up -d web nginx-proxy

# 验证 nginx 配置语法
docker compose -f deploy/docker-compose.prod.yml --env-file .env exec nginx-proxy nginx -t

# 服务器侧上线后切到 ssl conf 需要 reload:
# docker compose -f deploy/docker-compose.prod.yml --env-file .env exec nginx-proxy nginx -s reload
```

---

## 5. 验证

### 5.1 命令行 SSE

```bash
# 本地
curl -N -X POST http://localhost/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"想开个火锅店,装修要多少钱"}' --max-time 30

# 服务器
curl -N -X POST https://www.meikaizs.com/api/ai/chat ...
```

预期看到流式输出:
```
event: meta
data: {"conversation_id":"..."}

event: meta
data: {"business_line":"storefront"}

event: delta
data: {"text":"..."}
...
event: done
data: {}
```

### 5.2 浏览器 ChatWidget multi-turn

- 本地:打开 http://localhost(注意:`web` 在 prod compose 里没暴露端口,流量必须走 nginx-proxy 的 80)
- 服务器:打开 https://www.meikaizs.com

操作:
1. 点右下角 💬 悬浮按钮 → ChatPanel 弹出
2. 第一轮发"想开个火锅店,装修要多少钱"
   - 应识别 `business_line=storefront`
   - 流式吐字,末尾含「这只是 AI 输出的价格…」免责声明
3. 第二轮发"200 平米"
   - 应**直接出报价**(火锅店 × 200㎡),不再问业态
   - 这一步验证 multi-turn checkpointer:`conversation_id` 复用 → ai-service 加载上轮 slots

第 3 步不通 = checkpointer 链路断 → 看 ai-service 日志确认 saver 类型 + thread_id。

---

## 6. 常见踩坑

### 6.1 ai-service 启动日志见 `降级 InMemorySaver`

aiomysql 连不上 mysql。三种常见原因:
1. **mysql_data 卷密码漂移**(本地最常见):见 §4.1
2. **缺 cryptography**:已在 `pyproject.toml` 修复;若镜像 build 早于 2026-06-19,需 rebuild
3. **mysql 还没 healthy 就启 ai-service**:`depends_on: service_healthy` 已挡;手动 up 时先 §4.4 单独起 mysql

### 6.2 `/api/ai/chat` 返回 502 或挂住

- nginx 配置必须 `proxy_buffering off`(`edge.local.conf` / `edge.ssl.conf` 都已设);若改过本地副本检查
- ai-service healthcheck 是否通过:`docker compose ps ai-service` 看到 `(healthy)`
- 看 ai-service 日志:`docker compose logs -f ai-service`

### 6.3 浏览器 ChatWidget 提示 CORS 错误

`ALLOWED_ORIGINS` 与浏览器实际访问的 origin 不匹配。本地用 `http://localhost`(不含端口,因为 nginx-proxy 占 80);若你改用 8080 等其他端口,要补上 `http://localhost:8080`。

### 6.4 Qdrant 灌索引失败

- 检查 `QDRANT_API_KEY` 在两份 `.env` 是否一致
- 检查 `ai-service/data/projects_labeled.jsonl` 是否存在:
  `docker compose -f deploy/docker-compose.prod.yml --env-file .env run --rm --entrypoint sh ai-service -c 'ls -la data/'`
- 检查 Doubao Embedding endpoint 是否正确,在 Ark 控制台测试该 ep

### 6.5 ai-service OOM 被杀(仅服务器 2G 机型)

`mem_limit: 500m` 是按"去 PaddleOCR + 远程 Provider"测算的;若装了 `[local]` extras 会暴涨,务必保持 prod 镜像不装。LLM 上下文如果接近 32k 也可能瞬时撑爆。

---

## 7. 回滚

### 7.1 本地预演不通过

`docker compose -f deploy/docker-compose.prod.yml --env-file .env down -v` 清掉所有卷重来。代码改完重 build。

### 7.2 服务器线上故障

临时关掉 AI 客服:
```bash
docker compose -f deploy/docker-compose.prod.yml --env-file .env stop ai-service qdrant
# 网站其他功能不受影响,ChatWidget 调用会 502
```

数据库改动是幂等只增的(`CREATE TABLE IF NOT EXISTS`),无需回滚 schema。
