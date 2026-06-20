# DESIGN §13.2:已剔除 PaddleOCR;ODA File Converter 推到 Sprint 2 早期 spike
# 单阶段 slim 基底足够;镜像 ~250MB,留出 2GB 机器内存预算
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 系统依赖:python-magic 要 libmagic;httpx/aiomysql 走纯 Python
RUN apt-get update && apt-get install -y --no-install-recommends \
      libmagic1 \
      curl \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 非 root(DESIGN §10 表第 12 项)
RUN useradd -m -u 10001 -s /bin/bash appuser
WORKDIR /app

# 依赖先装,代码后拷,利用 docker 层缓存
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

# 业务代码
COPY app ./app
COPY schemas ./schemas
COPY knowledge ./knowledge

# OOM 优先级:让自己比 mysql 先被杀(DESIGN §13.2)
# 容器需配合 cap_add: SYS_RESOURCE
COPY <<'EOF' /app/entrypoint.sh
#!/usr/bin/env bash
set -e
echo 500 > /proc/self/oom_score_adj 2>/dev/null || true
exec uvicorn app.main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"
EOF
RUN chmod +x /app/entrypoint.sh && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://localhost:8000/healthz || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
