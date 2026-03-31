import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.path !== from.path) {
      return { top: 0, left: 0, behavior: 'smooth' }
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
    {
      path: '/contact',
      name: 'contact',
      component: () => import('@/views/Contact.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue'),
    },
  ],
})

export default router
