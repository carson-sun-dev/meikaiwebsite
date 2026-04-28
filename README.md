# 🌟 美恺装饰官网（meikaizs.com）

[![Live Site](https://img.shields.io/badge/Live-www.meikaizs.com-0ea5e9?style=flat-square)](https://www.meikaizs.com)
[![Frontend](https://img.shields.io/badge/Frontend-Vue%203%20%2B%20Vite-42b883?style=flat-square)](./frontend)
[![Backend](https://img.shields.io/badge/Backend-Node.js%20%2B%20Express-111827?style=flat-square)](./backend)
[![Database](https://img.shields.io/badge/Database-MySQL%208-4479A1?style=flat-square)](https://www.mysql.com/)

美恺装饰企业官网项目，已线上运行于 [www.meikaizs.com](https://www.meikaizs.com)。

项目采用前后端分离与容器化部署：  
- 前端为 Vue 3 单页站点（品牌展示 + 案例展示 + 联系/报价入口）  
- 后端提供留资接口（报价表单、页脚电话）  
- MySQL 持久化存储提交数据  
- Nginx 在生产环境负责 HTTPS 终止与反向代理  

---

## 🔗 在线访问

- 域名地址：<https://www.meikaizs.com>
- 支持页面：`/home`、`/store`、`/business`、`/residential`、`/contact`、`/about`

---

## ✨ 核心功能

- 🧩 品牌官网展示：公司介绍、业务方向、案例图集、发展历程
- 🏢 多业务线内容：店铺装修、商务办公、精品家装
- 📝 留资能力：  
  - ✅ 一键报价表单（`POST /api/leads/quote`）  
  - ✅ 页脚电话提交（`POST /api/leads/footer-phone`）
- 🔍 SEO 能力：路由级标题/描述/关键词、Canonical、Organization JSON-LD
- 🔄 同源 API 调用：前端默认请求 `/api`，由 Nginx/Dev Proxy 转发后端

---

## 🛠️ 技术栈

### 🎨 Frontend

- Vue 3 + TypeScript + Vite
- Vue Router、Pinia
- Element Plus
- Tailwind CSS（Vite 插件）
- Vitest（单测）+ Playwright（E2E）

### ⚙️ Backend

- Node.js + TypeScript
- Express
- Zod（请求校验）
- mysql2（连接 MySQL）

### 🚀 Deployment

- Docker + Docker Compose
- Nginx（静态托管 + 反代）
- Let's Encrypt（证书签发与续期）
- 腾讯云 CVM 生产部署（文档见 `deploy/TENCENT_CLOUD.md`）

---

## 🧱 系统架构

```text
Browser
  -> nginx-proxy (80/443, SSL terminate)
    -> web (Nginx, static frontend)
      -> /api reverse proxy
        -> backend (Express :3001)
          -> mysql (MySQL 8, volume persistence)
```

---

## 📁 目录结构

```text
meikai_website/
├─ frontend/                # Vue 3 前端
├─ backend/                 # Express + MySQL 后端
├─ deploy/                  # 生产部署与证书脚本
├─ docker-compose.yml       # 本地联调编排
├─ DEPLOY.md                # 快速部署说明
└─ README.md
```

---

## 💻 本地开发（不使用 Docker）

### 1) 🗄️ 启动 MySQL

可使用本机 MySQL，或只拉起数据库容器：

```bash
docker compose up -d mysql
```

### 2) ⚙️ 启动后端

```bash
cd backend
cp .env.example .env
pnpm install
pnpm dev
```

默认运行在 `http://127.0.0.1:3001`。

### 3) 🎨 启动前端

```bash
cd frontend
pnpm install
pnpm dev
```

Vite 开发环境会将 `/api` 代理到后端 `3001`。

---

## 🐳 Docker 一键联调

```bash
docker compose up -d --build
```

默认访问：<http://localhost:8080>

服务说明：
- 🌐 `web`：前端静态站点
- 🧠 `backend`：接口服务
- 🗃️ `mysql`：数据服务（卷：`mysql_data`）


---

## 📚 开发命令速查

### 🎨 Frontend（`frontend/`）

- ▶️ `pnpm dev`：启动开发服务器
- 🏗️ `pnpm build`：类型检查 + 构建
- 👀 `pnpm preview`：预览构建产物
- 🧪 `pnpm test:unit`：运行单元测试
- 🎭 `pnpm test:e2e`：运行端到端测试
- 🧹 `pnpm lint`：运行并修复 lint

### ⚙️ Backend（`backend/`）

- ▶️ `pnpm dev`：开发模式（watch）
- 🏗️ `pnpm build`：编译 TypeScript
- 🚢 `pnpm start`：运行编译产物


