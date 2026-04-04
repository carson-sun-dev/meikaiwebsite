# 美恺站点：启动与部署

## 架构说明

- **MySQL 8**：存留资数据（表 `submissions`：一键报价 + 页脚电话）。
- **backend**：Node + Express，`/api/*`。
- **web**：Nginx 托管 Vue 静态资源，并把 **`/api` 反代到 backend**（浏览器始终同源，无需改前端里的 `/api` 路径）。

---

## 一、本地开发（不跑 Docker）

### 1. 准备 MySQL

本机安装 MySQL 8，或只启动数据库容器：

```bash
cd meikai_website
docker compose up -d mysql
```

等 `mysql` healthy 后，库会自动创建（见 `docker-compose.yml` 里 `MYSQL_DATABASE`）。

### 2. 后端

```bash
cd backend
cp .env.example .env
# 编辑 .env：DATABASE_HOST=127.0.0.1，账号密码与 compose 或本机 MySQL 一致
pnpm install
pnpm dev
```

默认 API：`http://127.0.0.1:3001`。

### 3. 前端

```bash
cd frontend
pnpm install
pnpm dev
```

Vite 会把 `/api` 代理到 `http://127.0.0.1:3001`（见 `vite.config.ts`）。

---

## 二、一键 Docker（推荐联调 / 服务器）

在项目根目录 `meikai_website`：

```bash
cp .env.docker.example .env
# 修改 MYSQL_*、WEB_PORT、CORS_ORIGINS（生产务必改强密码）
docker compose up -d --build
```

浏览器访问：**`http://localhost:8080`**（若未改 `WEB_PORT`）。

- 页面上所有 `/api/...` 请求由 Nginx 转到容器 `backend`。
- 数据在卷 **`mysql_data`**，删卷相当于清空库。

查看日志：

```bash
docker compose logs -f backend web
```

更新后重新构建：

```bash
git pull
docker compose up -d --build
```

---

## 三、腾讯云上线（HTTPS 与生产 Compose）

完整步骤（防火墙、Let’s Encrypt、`.env` 模板）见 **`deploy/TENCENT_CLOUD.md`**。

概要：

1. **代码**：本机 `git push`，服务器 `git clone` / `git pull`（见上文「本机改代码后如何同步」）。
2. **安装 Docker**：Docker Engine + Compose 插件。
3. **配置**：服务器项目根目录 `.env`（可用 `deploy/env.prod.example`），**强密码** + `CORS_ORIGINS` 含 `https://www.你的域名` 与裸域。
4. **防火墙**：放行 **80、443**（及 SSH 22）；**不要**把 MySQL `3306` 暴露公网。
5. **启动**：`cp deploy/edge.http.conf deploy/edge.active.conf` 后  
   `docker compose -f deploy/docker-compose.prod.yml up -d --build`，再按文档跑 `deploy/init-letsencrypt.sh` 启用 HTTPS。

本地单机联调仍可用根目录 **`docker compose up -d --build`**（`http://localhost:8080`），与生产 **`deploy/docker-compose.prod.yml`** 是两套编排。

若前后端**拆分不同域名**，构建前端时需带 API 地址：

```bash
# 示例：仅当你把 API 单独挂在 https://api.example.com 时
docker compose build --build-arg VITE_API_BASE=https://api.example.com web
```

当前默认 **`VITE_API_BASE` 为空**，靠同域 `/api` 反代，一般无需设置。

---

## 四、接口备忘

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/leads/quote` | 一键报价表单 |
| POST | `/api/leads/footer-phone` | 页脚 `{ "phone": "..." }` |

---

## 五、从旧版 SQLite 迁移

若你本地还有 `backend/data/*.sqlite`，需自行导出或丢弃；上线 MySQL 后仅使用新库中的表结构（服务启动时会 `CREATE TABLE IF NOT EXISTS`）。
