# 腾讯云 CVM 部署说明（域名 www.meikaizs.com · 2 核 2G）

本文假设：已购买 **腾讯云轻量应用服务器或 CVM**（2C2G）、域名 **meikaizs.com** 已备案（如需 ICP），且 DNS 可在腾讯云解析中管理。

## 1. 架构说明

| 组件 | 说明 |
|------|------|
| **nginx-proxy** | 宿主机 **80/443**，终止 SSL，反代到 `web` |
| **web** | 前端静态资源 + 内嵌 Nginx，将 `/api` 转到 `backend` |
| **backend** | Node.js Express，仅内网 `3001` |
| **mysql** | MySQL 8，数据卷持久化，**不**映射到公网 |

生产 compose：`deploy/docker-compose.prod.yml`。开发本地仍可用根目录 `docker-compose.yml`。

## 2. 服务器准备

1. **系统**：推荐 Ubuntu 22.04 LTS 或 Debian 12。
2. **安全组 / 防火墙**：放行入站 **TCP 80、443**（SSH 22 仅对你本机 IP 开放更安全）。
3. **内存**：2G 较紧，建议加 **1–2G Swap**（腾讯云控制台或 `fallocate` + `mkswap`）。
4. **安装 Docker**（官方文档一键安装即可），并启用 `docker compose`（Docker Compose V2）。

## 3. 域名解析

在 **DNS** 中新增（指向 CVM **公网 IP**）：

- 记录类型 **A**：主机记录 `www`，值 `x.x.x.x`
- 记录类型 **A**：主机记录 `@`（裸域），值 `x.x.x.x`

等待解析生效后再申请证书（可用 `ping www.meikaizs.com` 看是否指向正确 IP）。

## 4. 代码与环境变量

```bash
cd /opt   # 或你喜欢的目录
git clone <你的仓库> meikai_website
cd meikai_website

cp deploy/env.prod.example .env
# 编辑 .env：MYSQL_ROOT_PASSWORD、MYSQL_PASSWORD 改为强密码；其余按注释检查
```

`CORS_ORIGINS` 必须包含：

`https://www.meikaizs.com,https://meikaizs.com`

否则浏览器在 HTTPS 下无法调用 `/api`。

### 本机改代码后如何同步到服务器

1. **本机**：在项目里 `git add` → `git commit` → `git push` 到 GitHub。  
2. **服务器**：`cd ~/meikaiwebsite`（目录名以你为准）→ `git pull`。  
3. **需要重新构建镜像时**（改了 `Dockerfile`、`docker-compose.prod.yml`、前后端依赖等）：

   ```bash
   sudo docker compose -f deploy/docker-compose.prod.yml up -d --build
   ```

   仅改 `.env` 时一般 `docker compose ... up -d` 即可（或 `restart` 对应服务）。

## 5. 首次启动与 SSL（Let’s Encrypt）

1. **复制边缘配置（HTTP 阶段，便于签发证书）**

   ```bash
   cp deploy/edge.http.conf deploy/edge.active.conf
   ```

2. **构建并启动**

   ```bash
   docker compose -f deploy/docker-compose.prod.yml build
   docker compose -f deploy/docker-compose.prod.yml up -d
   ```

   此时站点可通过 `http://www.meikaizs.com` 访问（尚无 HTTPS）。

3. **申请证书**（将邮箱换成你的，用于 Let's Encrypt 通知）

   ```bash
   export SSL_EMAIL=你的邮箱@example.com
   bash deploy/init-letsencrypt.sh
   ```

   脚本会：用 **webroot** 校验、`certonly` 申请 **www + 裸域**、把 `edge.ssl.conf` 拷为 `edge.active.conf` 并重载 **nginx-proxy**。

4. **验证**：浏览器打开 `https://www.meikaizs.com`，检查锁图标；测表单提交与页脚留资。

若申请失败：确认 **80** 端口从公网可访问、域名已指到本机、安全组放行。

### 使用腾讯云 SSL 证书（替代 Let's Encrypt）

将 Nginx 用的 **fullchain** / **privkey** 放到服务器目录，可挂载进 `nginx-proxy`（需自行改 `edge.ssl.conf` 里 `ssl_certificate` 路径并重建/重载）。一般仍推荐 Let's Encrypt + 自动续期。

## 6. 证书续期

Let’s Encrypt 有效期约 90 天。`certbot renew` 为续期命令；项目提供：

```bash
bash deploy/renew-cert.sh
```

建议 **crontab**（每天凌晨尝试续期）：

```cron
0 3 * * * cd /opt/meikai_website && ./deploy/renew-cert.sh >> /var/log/certbot-renew.log 2>&1
```

## 7. 常用运维命令

```bash
# 查看状态
docker compose -f deploy/docker-compose.prod.yml ps

# 日志
docker compose -f deploy/docker-compose.prod.yml logs -f backend

# 更新代码后重新构建前端/后端
docker compose -f deploy/docker-compose.prod.yml build --no-cache web backend
docker compose -f deploy/docker-compose.prod.yml up -d

# 数据库仅在 Docker 网络内；备份示例（在宿主机执行）
docker compose -f deploy/docker-compose.prod.yml exec mysql \
  mysqldump -u meikai -p"$MYSQL_PASSWORD" meikai > backup-$(date +%F).sql
```

（将 `meikai`、密码与库名与 `.env` 一致。）

## 8. 安全与优化摘要

- 生产后端已 **`trust proxy`**，便于经 Nginx 获取真实 IP。
- MySQL 在 compose 中限制 **innodb_buffer_pool≈256M** 等，适配 2G 机型；连接池在生产降为 **5**。
- 边缘 **HTTPS** 配置含 HSTS、基础安全头（见 `deploy/edge.ssl.conf`）。
- **勿**向公网暴露 `3306`；**勿**将含密码的 `.env` 提交 Git。

## 9. 与本地 `docker-compose.yml` 的区别

- 根目录 `docker-compose.yml`：适合本机开发，`web` 映射 `8080:80`，无最外层 SSL。
- `deploy/docker-compose.prod.yml`：增加 **nginx-proxy**、**443**、证书卷；**web / mysql / backend** 不直接暴露不必要端口。

更多环境变量示例见 `deploy/env.prod.example` 与仓库根目录 `.env.docker.example`。
