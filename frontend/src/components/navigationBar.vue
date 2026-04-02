<template>
  <header
    class="nav-bar"
    :class="{
      'nav-bar--contrast-normal': isHomeRoute && contrastMode === 'normal',
      'nav-bar--contrast-high': isHomeRoute && contrastMode === 'high',
      'nav-bar--solid-tall': isSolidNavBar,
    }"
    :style="{ background: navBackground }"
  >
    <nav class="nav-bar__wrap" aria-label="主导航">
      <!-- Frame：导航链接 -->
      <div class="nav-bar__links">
        <router-link class="nav-bar__link" to="/">网站首页</router-link>
        <router-link class="nav-bar__link" to="/store">品牌店装</router-link>
        <router-link class="nav-bar__link" to="/business">商务·办公</router-link>
        <router-link class="nav-bar__link" to="/residential">精品家装</router-link>
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
          <PaperPlaneIcon class="nav-bar__estimate-icon" />
          <span class="nav-bar__estimate-text">一键估价</span>
        </router-link>
      </div>

      <button type="button" class="nav-bar__lang" @click="onToggleLocale">中/EN</button>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'

import logoImg from '@/source/logo/logo.png'
import ziImg from '@/source/logo/zi.png'

const route = useRoute()
const props = withDefaults(
  defineProps<{
    contrastMode?: 'normal' | 'high'
  }>(),
  {
    contrastMode: 'normal',
  },
)
const isHomeRoute = computed(() => route.path === '/' || route.path === '/home')
const contrastMode = computed(() => props.contrastMode)

/** 黑底导航页（非首页、非关于）：加高黑色条区域 */
const isSolidNavBar = computed(() => {
  const p = route.path
  return p !== '/' && p !== '/home' && p !== '/about'
})

const navBackground = computed(() => {
  // 首页 / 关于我们需要透明融入 Hero；联系页及其他页面保持黑色。
  // 当前路由：`/` 会重定向到 `/home`，但这里同时兼容。
  return isHomeRoute.value || route.path === '/about' ? 'transparent' : '#000'
})

function onToggleLocale() {
  /* TODO */
}
</script>

<style scoped>
.nav-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  width: min(96%, 1280px);
  flex-shrink: 0;
  background: transparent;
  padding: 8px 0 11px;
  border-radius: 0 0 20px 20px;
  margin: 0 auto;
}

.nav-bar--contrast-normal {
  background: rgb(8 8 8 / 0.12);
}

.nav-bar--contrast-high {
  background: rgb(8 8 8 / 0.28);
}

.nav-bar--solid-tall {
  padding: 14px 0 18px;
}

.nav-bar__wrap {
  display: flex;
  max-width: 1080px;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 8px;
  box-sizing: border-box;
}

.nav-bar__links {
  display: flex;
  align-items: center;
  gap: 14px;
  font-family:
    'Manrope',
    'Noto Sans JP',
    system-ui,
    sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  letter-spacing: -0.14px;
  white-space: nowrap;
}

.nav-bar--contrast-high .nav-bar__links,
.nav-bar--contrast-high .nav-bar__contact,
.nav-bar--contrast-high .nav-bar__lang {
  text-shadow: 0 1px 6px rgb(0 0 0 / 0.75);
}

.nav-bar--contrast-high .nav-bar__contact::after {
  border-color: rgb(255 255 255 / 0.92);
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
  transform: translateX(28px);
}

.nav-bar__logo-link {
  position: relative;
  display: flex;
  height: 64px;
  width: 228px;
  align-items: center;
  padding-left: 8px;
  box-sizing: border-box;
  text-decoration: none;
}

.nav-bar__logo-mark {
  width: 68px;
  height: 64px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.nav-bar__logo-word {
  width: 132px;
  height: 64px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.nav-bar__cta {
  display: flex;
  width: 244px;
  flex-shrink: 0;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
}

.nav-bar__contact {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
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
  height: 34px;
  width: 112px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 14px;
  box-sizing: border-box;
  border-radius: 32px;
  background: #ff5449;
  font-family:
    'Inter',
    'Noto Sans JP',
    'Noto Sans SC',
    system-ui,
    sans-serif;
  font-size: 13px;
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
  width: 14px;
  height: 14px;
  color: #fff;
  transform: translateY(0.5px);
}

.nav-bar__estimate-text {
  display: block;
  line-height: 1;
  transform: translateY(0.5px);
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
  .nav-bar {
    width: 100%;
  }

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
