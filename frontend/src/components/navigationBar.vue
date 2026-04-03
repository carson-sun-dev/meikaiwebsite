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
      <!-- ≥901px：桌面横排 -->
      <div class="nav-bar__desktop">
        <div class="nav-bar__links">
          <router-link class="nav-bar__link" to="/">网站首页</router-link>
          <router-link class="nav-bar__link" to="/store">品牌店装</router-link>
          <router-link class="nav-bar__link" to="/business">商务·办公</router-link>
          <router-link class="nav-bar__link" to="/residential">精品家装</router-link>
        </div>

        <div class="nav-bar__brand">
          <router-link to="/home" class="nav-bar__logo-link" aria-label="美恺装饰">
            <img :src="logoImg" alt="" class="nav-bar__logo-mark" />
            <img :src="ziImg" alt="美恺装饰" class="nav-bar__logo-word" />
          </router-link>
        </div>

        <div class="nav-bar__cta">
          <router-link class="nav-bar__contact" to="/about">关于美恺</router-link>
          <router-link class="nav-bar__estimate" to="/contact">
            <PaperPlaneIcon class="nav-bar__estimate-icon" />
            <span class="nav-bar__estimate-text">一键估价</span>
          </router-link>
        </div>
      </div>

      <!-- ≤900px：顶栏 + 可折叠菜单 -->
      <div class="nav-bar__mobile-bar">
        <button
          type="button"
          class="nav-bar__burger"
          :aria-expanded="menuOpen"
          aria-controls="nav-mobile-drawer"
          aria-label="展开或收起导航"
          @click="menuOpen = !menuOpen"
        >
          <span class="nav-bar__burger-box" aria-hidden="true">
            <span class="nav-bar__burger-line" />
            <span class="nav-bar__burger-line" />
            <span class="nav-bar__burger-line" />
          </span>
        </button>

        <div class="nav-bar__mobile-brand">
          <router-link to="/home" class="nav-bar__logo-link nav-bar__logo-link--compact" aria-label="美恺装饰">
            <img :src="logoImg" alt="" class="nav-bar__logo-mark" />
            <img :src="ziImg" alt="美恺装饰" class="nav-bar__logo-word" />
          </router-link>
        </div>

        <router-link class="nav-bar__estimate nav-bar__estimate--toolbar" to="/contact" @click="closeMenu">
          <PaperPlaneIcon class="nav-bar__estimate-icon" />
          <span class="nav-bar__estimate-text">一键估价</span>
        </router-link>
      </div>

      <div
        v-show="menuOpen"
        id="nav-mobile-drawer"
        class="nav-bar__mobile-drawer"
      >
        <router-link class="nav-bar__mobile-link" to="/" @click="closeMenu">网站首页</router-link>
        <router-link class="nav-bar__mobile-link" to="/store" @click="closeMenu">品牌店装</router-link>
        <router-link class="nav-bar__mobile-link" to="/business" @click="closeMenu">商务·办公</router-link>
        <router-link class="nav-bar__mobile-link" to="/residential" @click="closeMenu">精品家装</router-link>
        <router-link class="nav-bar__mobile-link nav-bar__mobile-link--secondary" to="/about" @click="closeMenu">
          关于美恺
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'

import logoImg from '@/source/logo/logo.png'
import ziImg from '@/source/logo/zi.png'

const route = useRoute()
const menuOpen = ref(false)

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
  return isHomeRoute.value || route.path === '/about' ? 'transparent' : '#000'
})

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false
  },
)

function closeMenu() {
  menuOpen.value = false
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    menuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
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
  flex-direction: column;
  align-items: stretch;
  gap: 0;
  max-width: 1080px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 8px;
  box-sizing: border-box;
}

.nav-bar__desktop {
  display: none;
  width: 100%;
  align-items: center;
  box-sizing: border-box;
  /* 左右栏等宽占位，中间 logo 相对整条导航水平居中 */
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  column-gap: 18px;
}

.nav-bar__links {
  justify-self: start;
  min-width: 0;
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
.nav-bar--contrast-high .nav-bar__contact {
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
  justify-self: center;
  flex-shrink: 0;
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
  justify-self: end;
  display: flex;
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

/* —— 移动端顶栏与抽屉 —— */
.nav-bar__mobile-bar {
  display: none;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  width: 100%;
  min-height: 52px;
  box-sizing: border-box;
}

.nav-bar__burger {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  margin: 0;
  padding: 0;
  border: none;
  border-radius: 10px;
  background: rgb(255 255 255 / 0.12);
  cursor: pointer;
  color: #fff;
}

.nav-bar__burger:hover {
  background: rgb(255 255 255 / 0.18);
}

.nav-bar__burger-box {
  display: flex;
  width: 20px;
  flex-direction: column;
  align-items: stretch;
  gap: 5px;
}

.nav-bar__burger-line {
  display: block;
  height: 2px;
  border-radius: 1px;
  background: currentcolor;
}

.nav-bar__mobile-brand {
  display: flex;
  min-width: 0;
  flex: 1;
  align-items: center;
  justify-content: center;
}

.nav-bar__logo-link--compact {
  height: 48px;
  width: min(200px, 44vw);
  padding-left: 4px;
}

.nav-bar__logo-link--compact .nav-bar__logo-mark {
  width: 50px;
  height: 48px;
}

.nav-bar__logo-link--compact .nav-bar__logo-word {
  width: 96px;
  height: 48px;
}

.nav-bar__estimate--toolbar {
  width: auto;
  min-width: 100px;
  height: 36px;
  padding: 6px 12px;
  font-size: 12px;
}

.nav-bar__mobile-drawer {
  display: flex;
  width: 100%;
  flex-direction: column;
  gap: 2px;
  margin-top: 6px;
  padding: 10px 6px 12px;
  box-sizing: border-box;
  border-top: 1px solid rgb(255 255 255 / 0.18);
  background: rgb(0 0 0 / 0.35);
  backdrop-filter: blur(10px);
  border-radius: 0 0 14px 14px;
}

.nav-bar__mobile-link {
  display: flex;
  min-height: 48px;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 10px;
  font-family:
    'Manrope',
    'Noto Sans SC',
    system-ui,
    sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  text-decoration: none;
}

.nav-bar__mobile-link:hover {
  background: rgb(255 255 255 / 0.08);
}

.nav-bar__mobile-link--secondary {
  margin-top: 4px;
  border: 1px solid rgb(255 255 255 / 0.35);
  font-weight: 600;
}

@media (min-width: 901px) {
  .nav-bar {
    width: min(96%, 1280px);
  }

  .nav-bar__wrap {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
  }

  .nav-bar__desktop {
    display: grid;
  }

  .nav-bar__mobile-bar,
  .nav-bar__mobile-drawer {
    display: none !important;
  }
}

@media (max-width: 900px) {
  .nav-bar {
    width: 100%;
  }

  .nav-bar__mobile-bar {
    display: flex;
  }
}

@media (prefers-reduced-motion: reduce) {
  .nav-bar__estimate:hover {
    filter: none;
  }
}
</style>
