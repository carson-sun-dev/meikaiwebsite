import { fileURLToPath, URL } from 'node:url'

import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  base: '/', // 显式声明根路径
  plugins: [
    vue(),
    // 仅 dev server 启用；生产 build / vitest 不打包 DevTools
    ...(process.env.NODE_ENV === 'development' ? [vueDevTools()] : []),
    tailwindcss(),
  ],
  server: {
    proxy: {
      // 所有 /api/* 走 docker 的 nginx-proxy(80 端口),由 nginx 内部路由:
      //   /api/ai/*  → ai-service:8000
      //   /api/*     → backend:3001
      // 这样 vite dev 跟生产路由 100% 一致;同时 SSE/buffer 设置走 nginx 已配的 proxy_buffering off。
      // 前提:本机起着 docker compose(至少 nginx-proxy + ai-service + backend + mysql + qdrant)
      '/api': {
        target: 'http://127.0.0.1',
        changeOrigin: true,
        // SSE 长连接要求保活
        timeout: 0,
        proxyTimeout: 0,
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@source': fileURLToPath(new URL('../source', import.meta.url)),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/vue-router')) return 'vue-router'
          if (id.includes('/components/ChatWidget/')) return 'chat-widget'
        },
      },
    },
  },
})
