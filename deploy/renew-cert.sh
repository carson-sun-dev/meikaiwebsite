#!/usr/bin/env bash
# 建议 crontab：0 3 * * * /path/to/meikai_website/deploy/renew-cert.sh >> /var/log/certbot-renew.log 2>&1
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

docker compose -f deploy/docker-compose.prod.yml --profile tools run --rm certbot renew
docker compose -f deploy/docker-compose.prod.yml exec nginx-proxy nginx -s reload
echo "$(date -Iseconds) cert renew ok"
