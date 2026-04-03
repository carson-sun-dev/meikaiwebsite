FROM node:22-bookworm-slim AS build

WORKDIR /app
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

COPY package.json pnpm-lock.yaml ./
# 与 package.json 中 packageManager 保持一致，避免与 lockfile 的 pnpm 版本指纹不一致
RUN corepack enable && corepack prepare pnpm@10.32.1 --activate
RUN pnpm install --frozen-lockfile

COPY . .

ARG VITE_API_BASE=
ENV VITE_API_BASE=$VITE_API_BASE

ARG VITE_SITE_ORIGIN=https://www.meikaizs.com
ENV VITE_SITE_ORIGIN=$VITE_SITE_ORIGIN

# 直接 vite build：避免 run-p / vue-tsc --build 在容器里对 workspace 解析踩坑
RUN pnpm exec vite build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
