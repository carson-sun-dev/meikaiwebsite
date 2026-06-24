import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, left: 0 }
  },
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/store',
      name: 'store',
      component: () => import('@/views/Store.vue'),
    },
    {
      path: '/business',
      name: 'business',
      component: () => import('@/views/Business.vue'),
    },
    {
      path: '/residential',
      name: 'residential',
      component: () => import('@/views/Residential.vue'),
    },
    // /contact 路由已废除(2026-06-22):所有 CTA 改为开 AI 客服 ChatPanel,
    // Contact.vue 文件保留在 views/ 不删,以便未来需要时恢复。
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue'),
    },
  ],
})

export default router
