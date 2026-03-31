<template>
  <header class="nav-bar" :style="{ background: navBackground }">
    <nav class="nav-bar__wrap" aria-label="主导航">
      <!-- Frame：导航链接 -->
      <div class="nav-bar__links">
        <router-link class="nav-bar__link nav-bar__link--underline" to="/">网站首页</router-link>
        <router-link class="nav-bar__link nav-bar__link--underline" to="/store">品牌店装</router-link>
        <span class="nav-bar__muted">商务·办公</span>
        <span class="nav-bar__muted">精品家装</span>
      </div>

      <!-- Frame1：Logo -->
      <div class="nav-bar__brand">
        <router-link to="/home" class="nav-bar__logo-link" aria-label="美恺装饰">
          <img :src="logoImg" alt="" class="nav-bar__logo-mark" />
          <img :src="ziImg" alt="美恺装饰" class="nav-bar__logo-word" />
        </router-link>
      </div>

      <!-- Frame2：关于美恺 + 一键估价 -->
      <div class="nav-bar__cta">
        <router-link class="nav-bar__contact" to="/about">关于美恺</router-link>
        <router-link class="nav-bar__estimate" to="/contact">
          <ChatPlusLight class="nav-bar__estimate-icon" />
          <span>一键估价</span>
        </router-link>
      </div>

      <button type="button" class="nav-bar__lang" @click="onToggleLocale">中/EN</button>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import ChatPlusLight from '@/components/icons/ChatPlusLight.vue'

import logoImg from '@source/logo/logo.png'
import ziImg from '@source/logo/zi.png'

const route = useRoute()

const navBackground = computed(() => {
  // 首页 / 关于我们需要透明融入 Hero；联系页及其他页面保持黑色。
  // 当前路由：`/` 会重定向到 `/home`，但这里同时兼容。
  return route.path === '/' || route.path === '/home' || route.path === '/about' ? 'transparent' : '#000'
})

function onToggleLocale() {
  /* TODO */
}
</script>

<style scoped>
.nav-bar {
  position: relative;
  z-index: 50;
  width: 100%;
  flex-shrink: 0;
  background: transparent;
  padding: 14px 0;
}

.nav-bar__wrap {
  display: flex;
  max-width: 1080px;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 40px 51px;
  margin-left: auto;
  margin-right: auto;
}

.nav-bar__links {
  display: flex;
  align-items: center;
  gap: 20px;
  font-family:
    'Manrope',
    'Noto Sans JP',
    system-ui,
    sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  letter-spacing: -0.14px;
  white-space: nowrap;
}

.nav-bar__link {
  color: inherit;
  text-decoration: none;
  cursor: pointer;
}

.nav-bar__link--underline {
  text-decoration: underline;
  text-decoration-skip-ink: none;
}

.nav-bar__muted {
  cursor: default;
}

.nav-bar__brand {
  flex-shrink: 0;
}

.nav-bar__logo-link {
  display: flex;
  height: 74px;
  width: 262px;
  align-items: center;
  padding-left: 10px;
  box-sizing: border-box;
  text-decoration: none;
}

.nav-bar__logo-mark {
  width: 80px;
  height: 74px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.nav-bar__logo-word {
  width: 150px;
  height: 74px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.nav-bar__cta {
  display: flex;
  width: 290px;
  flex-shrink: 0;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.nav-bar__contact {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-radius: 20px;
  font-family:
    'Manrope',
    'Noto Sans JP',
    'Noto Sans SC',
    system-ui,
    sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  letter-spacing: -0.14px;
  text-decoration: none;
  white-space: nowrap;
}

.nav-bar__contact::after {
  content: '';
  position: absolute;
  inset: 0;
  border: 2px solid #fff;
  border-radius: 20px;
  pointer-events: none;
}

.nav-bar__estimate {
  display: inline-flex;
  height: 36px;
  width: 105px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 10px 20px 10px 15px;
  box-sizing: border-box;
  border-radius: 32px;
  background: #ff5449;
  font-family:
    'Inter',
    'Noto Sans JP',
    'Noto Sans SC',
    system-ui,
    sans-serif;
  font-size: 12px;
  font-weight: 700;
  font-style: normal;
  line-height: normal;
  color: #fff;
  text-decoration: none;
  white-space: nowrap;
}

.nav-bar__estimate-icon {
  display: block;
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  position: relative;
}

.nav-bar__estimate:hover {
  filter: brightness(1.05);
}

.nav-bar__lang {
  border: none;
  padding: 0;
  background: none;
  font-family:
    'Manrope',
    'Noto Sans JP',
    system-ui,
    sans-serif;
  font-size: 16px;
  font-weight: 500;
  line-height: 1.2;
  color: #fff;
  letter-spacing: -0.16px;
  white-space: nowrap;
  cursor: pointer;
}

.nav-bar__lang:hover {
  opacity: 0.9;
}

@media (max-width: 900px) {
  .nav-bar__wrap {
    flex-direction: column;
    gap: 24px;
  }

  .nav-bar__cta {
    width: 100%;
    justify-content: center;
  }

  .nav-bar__links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
