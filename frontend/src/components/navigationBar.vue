<template>
  <header
    class="nav-bar"
    :class="{
      'nav-bar--scrolled': isScrolled,
    }"
  >
    <nav ref="navWrapRef" class="nav-bar__wrap" aria-label="主导航">
      <!-- ≥901px:桌面横排 — 左 logo / 中链接 / 右 CTA(圆弧) -->
      <div class="nav-bar__desktop">
        <div class="nav-bar__brand">
          <router-link to="/home" class="nav-bar__logo-link" aria-label="美恺装饰">
            <img :src="logoImg" alt="" class="nav-bar__logo-mark" />
            <img :src="ziImg" alt="美恺装饰" class="nav-bar__logo-word" />
          </router-link>
        </div>

        <div class="nav-bar__links">
          <router-link class="nav-bar__link" to="/">网站首页</router-link>
          <router-link class="nav-bar__link" to="/store">品牌店装</router-link>
          <router-link class="nav-bar__link" to="/business">商务办公</router-link>
          <router-link class="nav-bar__link" to="/residential">精品家装</router-link>
        </div>

        <div class="nav-bar__cta">
          <router-link class="nav-bar__contact" to="/about">关于美恺</router-link>
          <a class="nav-bar__estimate" href="javascript:void(0)" role="button" @click="openChat">
            <PaperPlaneIcon class="nav-bar__estimate-icon" />
            <span class="nav-bar__estimate-text">一键估价</span>
          </a>
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

        <a class="nav-bar__estimate nav-bar__estimate--toolbar" href="javascript:void(0)" role="button" @click="() => { closeMenu(); openChat(); }">
          <PaperPlaneIcon class="nav-bar__estimate-icon" />
          <span class="nav-bar__estimate-text">一键估价</span>
        </a>
      </div>

      <div
        v-show="menuOpen"
        id="nav-mobile-drawer"
        class="nav-bar__mobile-drawer"
      >
        <router-link
          class="nav-bar__mobile-link"
          :class="{ 'nav-bar__mobile-link--active': isCurrentRoute('/home') }"
          to="/home"
          @click="closeMenu"
        >
          网站首页
        </router-link>
        <router-link
          class="nav-bar__mobile-link"
          :class="{ 'nav-bar__mobile-link--active': isCurrentRoute('/store') }"
          to="/store"
          @click="closeMenu"
        >
          品牌店装
        </router-link>
        <router-link
          class="nav-bar__mobile-link"
          :class="{ 'nav-bar__mobile-link--active': isCurrentRoute('/business') }"
          to="/business"
          @click="closeMenu"
        >
          商务·办公
        </router-link>
        <router-link
          class="nav-bar__mobile-link"
          :class="{ 'nav-bar__mobile-link--active': isCurrentRoute('/residential') }"
          to="/residential"
          @click="closeMenu"
        >
          精品家装
        </router-link>
        <router-link
          class="nav-bar__mobile-link nav-bar__mobile-link--secondary"
          :class="{ 'nav-bar__mobile-link--active': isCurrentRoute('/about') }"
          to="/about"
          @click="closeMenu"
        >
          关于美恺
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import { useChatWidget } from '@/composables/useChatWidget'

import logoImg from '@/source/logo/logo.webp'
import ziImg from '@/source/logo/zi.webp'

const route = useRoute()
const menuOpen = ref(false)
const navWrapRef = ref<HTMLElement | null>(null)
const isScrolled = ref(false)

// 用户反馈:nav 在所有页面都默认透明,滚动 60px 后变米灰毛玻璃。
// 原 isHomeRoute/isSolidNavBar/navBackground/contrastMode 强制非 home 页面黑底逻辑全部移除。
const { open: openChat } = useChatWidget()

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false
  },
)

function closeMenu() {
  menuOpen.value = false
}

function isCurrentRoute(path: string) {
  if (path === '/home') {
    return route.path === '/' || route.path === '/home'
  }
  return route.path === path
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    menuOpen.value = false
  }
}

function onPointerDown(e: PointerEvent) {
  if (!menuOpen.value) return
  const target = e.target
  if (!(target instanceof Node)) return
  if (navWrapRef.value?.contains(target)) return
  menuOpen.value = false
}

function onScroll() {
  isScrolled.value = window.scrollY > 60
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  window.addEventListener('pointerdown', onPointerDown)
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  window.removeEventListener('pointerdown', onPointerDown)
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.nav-bar {
  /* 全局 fixed:任何页面任何滚动位置都浮在视口顶部 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  width: 100%;
  flex-shrink: 0;
  background: transparent;
  padding: 10px 0 12px;
  margin: 0;
  transition: background-color 0.4s ease, backdrop-filter 0.4s ease, box-shadow 0.4s ease, padding 0.3s ease;
}

/* v2 风格 scrolled 状态:滚动 60px 后米灰半透明 + 毛玻璃 + 链接转墨黑 */
.nav-bar--scrolled {
  background: rgba(245, 242, 236, 0.92) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.08), 0 6px 24px rgba(0, 0, 0, 0.05);
  padding: 6px 0 8px;
}
.nav-bar--scrolled .nav-bar__links { color: #1a1a1a !important; }
.nav-bar--scrolled .nav-bar__contact { color: #1a1a1a !important; }
.nav-bar--scrolled .nav-bar__contact::after { border-color: #1a1a1a !important; }
/* scrolled 状态下汉堡按钮 — 用透明底 + 墨黑线条,避免灰黑块在米灰底突兀(用户反馈) */
.nav-bar--scrolled .nav-bar__burger {
  background: transparent !important;
  color: #1a1a1a !important;
}
.nav-bar--scrolled .nav-bar__burger:hover {
  background: rgba(196, 30, 58, 0.08) !important;
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
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0;
  max-width: none;
  margin-left: 0;
  margin-right: 0;
  /* 留出舒适的左右 margin,但不像之前 max-width:1080 那样太窄(用户反馈持续调) */
  padding: 0 clamp(32px, 5vw, 80px);
  box-sizing: border-box;
}
@media (max-width: 768px) {
  .nav-bar__wrap { padding: 0 20px; }
}

.nav-bar__desktop {
  display: none;
  width: 100%;
  align-items: center;
  box-sizing: border-box;
  /* 重排:左 logo / 中 links(自动撑大) / 右 CTA */
  grid-template-columns: auto minmax(0, 1fr) auto;
  column-gap: 24px;
}

.nav-bar__links {
  justify-self: center;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: nowrap;
  gap: clamp(12px, 2vw, 28px);
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  font-size: clamp(13px, 1.1vw, 16px);
  font-weight: 500;
  line-height: 1.2;
  color: #fff;
  letter-spacing: 0.08em;
  white-space: nowrap;
  overflow: hidden;
}

.nav-bar__link {
  position: relative;
  padding: 6px 2px;
  transition: opacity 0.3s ease;
}
.nav-bar__link::after {
  content: '';
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s cubic-bezier(0.2, 0.85, 0.3, 1);
}
.nav-bar__link:hover::after { transform: scaleX(1); }

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
  justify-self: start;
  flex-shrink: 0;
}

.nav-bar__logo-link {
  position: relative;
  display: flex;
  height: 56px;
  width: 200px;
  align-items: center;
  padding-left: 0;
  box-sizing: border-box;
  text-decoration: none;
}

.nav-bar__logo-mark {
  width: 56px;
  height: 52px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.nav-bar__logo-word {
  width: 120px;
  height: 52px;
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
  gap: 10px;
}

.nav-bar__contact {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  height: 36px;
  min-width: 96px;
  padding: 0 14px;
  border-radius: 999px;
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
  border-radius: 999px;
  pointer-events: none;
}

.nav-bar__estimate {
  display: inline-flex;
  height: 36px;
  min-width: 96px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 0 14px;
  box-sizing: border-box;
  /* 圆弧 pill 形(用户指定) */
  border-radius: 999px;
  background: #c41e3a;
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  line-height: 1;
  color: #fff;
  text-decoration: none;
  white-space: nowrap;
  box-shadow: 0 4px 14px rgba(196, 30, 58, 0.32), inset 0 0 0 1px #8b1424;
  transition: background-color 0.3s ease, transform 0.3s cubic-bezier(0.2, 0.85, 0.3, 1.05),
              box-shadow 0.3s ease;
}
.nav-bar__estimate:hover {
  background: #8b1424;
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(196, 30, 58, 0.4), inset 0 0 0 1px #8b1424;
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
  padding-bottom: 2px;
}

/* hover 已在 .nav-bar__estimate 主规则中处理(背景+位移+阴影) */

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
  transform: translateX(6%);
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
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  z-index: 40;
  display: flex;
  flex-direction: column;
  gap: 2px;
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

.nav-bar__mobile-link--active {
  background: rgb(255 255 255 / 0.18);
  box-shadow: 0 0 0 1px rgb(255 255 255 / 0.35) inset;
  font-weight: 600;
}

.nav-bar__mobile-link--secondary {
  margin-top: 4px;
  font-weight: 600;
}

@media (min-width: 901px) {
  .nav-bar {
    width: 100%;
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
    grid-template-columns: minmax(0, auto) minmax(0, 1fr) minmax(0, auto);
    column-gap: clamp(12px, 2vw, 24px);
  }

  .nav-bar__mobile-bar,
  .nav-bar__mobile-drawer {
    display: none !important;
  }
}

/* 901–1120px：进一步收紧，避免链接与 CTA 重叠 */
@media (min-width: 901px) and (max-width: 1120px) {
  .nav-bar__wrap {
    padding: 0 clamp(16px, 3vw, 32px);
  }

  .nav-bar__logo-link {
    width: 176px;
    height: 48px;
  }

  .nav-bar__logo-mark {
    width: 48px;
    height: 44px;
  }

  .nav-bar__logo-word {
    width: 104px;
    height: 44px;
  }

  .nav-bar__links {
    gap: 10px;
    font-size: 13px;
    letter-spacing: 0.04em;
  }

  .nav-bar__link {
    padding: 6px 0;
  }

  .nav-bar__contact,
  .nav-bar__estimate {
    height: 34px;
    min-width: 88px;
    padding: 0 12px;
    font-size: 12px;
  }

  .nav-bar__estimate-icon {
    width: 12px;
    height: 12px;
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
  .nav-bar__estimate:hover { transform: none; }
  .nav-bar__link::after { transition: none; }
}
</style>
