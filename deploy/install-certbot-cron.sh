#!/usr/bin/env bash
# 在服务器项目根目录执行：bash deploy/install-certbot-cron.sh
# 为 Let's Encrypt 证书添加每日自动续期（需当前用户可直接 docker，见下）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! docker info &>/dev/null; then
  echo "当前用户无法直接执行 docker，cron 里调用 renew-cert.sh 会失败。"
  echo "请先: sudo usermod -aG docker \"\$USER\" ，然后重新登录 SSH，再运行本脚本。"
  echo "或手动 crontab -e，参考 deploy/certbot-renew.crontab.example"
  exit 1
fi

LOG=/var/log/certbot-renew.log
if [[ ! -w "$(dirname "$LOG")" ]] 2>/dev/null; then
  LOG="$HOME/certbot-renew.log"
  echo "无权限写 /var/log，续期日志将写入: $LOG"
fi

LINE="0 3 * * * cd $ROOT && bash $ROOT/deploy/renew-cert.sh >> $LOG 2>&1"

if crontab -l 2>/dev/null | grep -qF "deploy/renew-cert.sh"; then
  (crontab -l 2>/dev/null | grep -vF "deploy/renew-cert.sh"; echo "$LINE") | crontab -
  echo "已更新续期任务。"
else
  (crontab -l 2>/dev/null; echo "$LINE") | crontab -
  echo "已添加续期任务。"
fi

echo "当前 crontab："
crontab -l
