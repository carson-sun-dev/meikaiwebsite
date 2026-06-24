import { createApp } from 'vue'
import { createHead } from '@unhead/vue/client'

import './assets/main.css'
// 全局 design tokens + mk-* + inner-* 内页通用样式;让所有 View 都能用 .mk-btn / .inner-* / .mk-section
import './views/home-page.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const head = createHead()

app.use(head)
app.use(router)

app.mount('#app')
