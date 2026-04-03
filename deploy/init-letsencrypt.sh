#!/usr/bin/env bash
# 在仓库根目录执行：bash deploy/init-letsencrypt.sh
# 需已解析域名到本机公网 IP，且防火墙放行 80/443
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export SSL_EMAIL="${SSL_EMAIL:?请先设置: export SSL_EMAIL=你的邮箱}"

if [[ ! -f deploy/edge.active.conf ]]; then
  cp deploy/edge.http.conf deploy/edge.active.conf
  echo "已创建 deploy/edge.active.conf（HTTP 模式）"
fi

docker compose -f deploy/docker-compose.prod.yml up -d

docker compose -f deploy/docker-compose.prod.yml --profile tools run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d www.meikaizs.com \
  -d meikaizs.com \
  --email "$SSL_EMAIL" \
  --agree-tos \
  --non-interactive \
  --no-eff-email

cp deploy/edge.ssl.conf deploy/edge.active.conf
docker compose -f deploy/docker-compose.prod.yml exec nginx-proxy nginx -s reload

echo "Let's Encrypt 证书已配置，请访问 https://www.meikaizs.com 验证。"
