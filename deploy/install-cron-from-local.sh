#!/usr/bin/env bash
# 在 Mac / 本机终端执行：通过 SSH 在「服务器」上安装证书自动续期 cron
#（证书与 Docker 均在云端，续期任务必须在服务器上跑，不能只配在本机 Mac）
#
# 用法：
#   export MEIKAI_SSH=ubuntu@你的公网IP
#   export MEIKAI_REMOTE_DIR=~/meikaiwebsite   # 可选，默认此项
#   bash deploy/install-cron-from-local.sh
#
# 需已配置 SSH 公钥登录；远端用户需能直接执行 docker（见 install-certbot-cron.sh）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

: "${MEIKAI_SSH:?请设置: export MEIKAI_SSH=ubuntu@服务器公网IP}"
REMOTE_DIR="${MEIKAI_REMOTE_DIR:-~/meikaiwebsite}"

echo "将在远端 $MEIKAI_SSH 的 $REMOTE_DIR 执行 deploy/install-certbot-cron.sh …"
ssh "$MEIKAI_SSH" "cd $REMOTE_DIR && bash deploy/install-certbot-cron.sh"
