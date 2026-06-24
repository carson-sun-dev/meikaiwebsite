<template>
  <section class="hero" aria-label="美恺装饰 · 主视觉">
    <!-- LQIP 模糊底图(浏览器解析 CSS 即可显示,大图加载完前不白屏) -->
    <div class="hero-base" aria-hidden="true"></div>

    <!-- 大图层:7 张轮播,每张响应式 -->
    <div class="hero-bg" aria-hidden="true">
      <img
        class="hero-preload"
        :src="firstSlideImage"
        alt=""
        aria-hidden="true"
        fetchpriority="high"
        loading="eager"
        decoding="async"
      />
      <div
        v-for="(slide, i) in slides"
        :key="`hero-bg-${i}`"
        class="hero-bg-layer"
        :class="{ 'hero-bg-layer--active': i === activeIndex }"
        :style="getSlideStyle(i, slide)"
      />
    </div>

    <!-- v2 蒙版:上方深 → 中段透 → 底部融入米灰背景(无硬切割) -->
    <div class="hero-mask" aria-hidden="true"></div>

    <!-- NavigationBar 已提到 App.vue 全局 fixed 顶部,本组件不再引用(2026-06-22) -->

    <!-- 主标题区:Z 字标题 + pill 紧贴 subtitle 下方右侧 -->
    <div class="hero-inner">
      <div class="hero-tag">郑 州 美 恺 装 饰</div>
      <h1 class="hero-title">
        <!-- Z 字结构:第二行向右偏移 2em,让"筑"和"心"垂直对齐;不再加朱红色块(用户反馈) -->
        <span class="hero-title__line hero-title__line--1">以匠心</span>
        <span class="hero-title__line hero-title__line--2">筑非凡</span>
      </h1>
      <p class="hero-subtitle">家装  ·  店铺  ·  办公</p>

      <!-- pill 比 subtitle 低一行,右对齐;整张点击开 AI 客服 -->
      <button
        type="button"
        class="hero-pill-pos"
        aria-label="即刻联系客服咨询"
        @click="onPillClick"
      >
        <HeroQuoteSearchPill
          :messages="pillMessages"
          :active-index="activeMessageIndex"
          @search="onPillClick"
        />
      </button>
    </div>

    <div class="hero-scroll-indicator" aria-hidden="true">下滑探索 ↓</div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import HeroQuoteSearchPill from './HeroQuoteSearchPill.vue'
import { useChatWidget } from '@/composables/useChatWidget'

// --- PC 高清 (首张 store1 走 public 固定路径与 index.html preload 共享缓存) ---
import imgBus1_PC from '@/source/homepage/1/pc/bussiness1.webp'
import imgBus3_PC from '@/source/homepage/1/pc/bussiness3.webp'
import imgHome1_PC from '@/source/homepage/1/pc/home1.webp'
import imgHome2_PC from '@/source/homepage/1/pc/home2.webp'
import imgStore2_PC from '@/source/homepage/1/pc/store2.webp'
import imgStore3_PC from '@/source/homepage/1/pc/store3.webp'

import imgBus1_T from '@/source/homepage/1/tablet/bussiness1.webp'
import imgBus3_T from '@/source/homepage/1/tablet/bussiness3.webp'
import imgHome1_T from '@/source/homepage/1/tablet/home1.webp'
import imgHome2_T from '@/source/homepage/1/tablet/home2.webp'
import imgStore2_T from '@/source/homepage/1/tablet/store2.webp'
import imgStore3_T from '@/source/homepage/1/tablet/store3.webp'

import imgBus1_M from '@/source/homepage/1/mobile/bussiness1.webp'
import imgBus3_M from '@/source/homepage/1/mobile/bussiness3.webp'
import imgHome1_M from '@/source/homepage/1/mobile/home1.webp'
import imgHome2_M from '@/source/homepage/1/mobile/home2.webp'
import imgStore2_M from '@/source/homepage/1/mobile/store2.webp'
import imgStore3_M from '@/source/homepage/1/mobile/store3.webp'

const imgStore1_PC = '/hero-lcp-pc.webp'
const imgStore1_T = '/hero-lcp-tablet.webp'
const imgStore1_M = '/hero-lcp-mobile.webp'

const HERO_CAROUSEL_INTERVAL_MS = 4500

const { open: openChat } = useChatWidget()

type HeroSlide = {
  pc: string
  tablet: string
  mobile: string
  message: string
  navContrast: 'normal' | 'high'
}

const slides: readonly HeroSlide[] = [
  { pc: imgStore1_PC, tablet: imgStore1_T, mobile: imgStore1_M, message: '店铺不歇业,改造能否进行?', navContrast: 'high' },
  { pc: imgBus1_PC,   tablet: imgBus1_T,   mobile: imgBus1_M,   message: '商务办公翻新,如何高效落地?',     navContrast: 'normal' },
  { pc: imgHome1_PC,  tablet: imgHome1_T,  mobile: imgHome1_M,  message: '家装设计施工,多久可以入住?',     navContrast: 'high' },
  { pc: imgStore2_PC, tablet: imgStore2_T, mobile: imgStore2_M, message: '店铺装饰怎么做更吸引顾客?', navContrast: 'high' },
  { pc: imgBus3_PC,   tablet: imgBus3_T,   mobile: imgBus3_M,   message: '办公空间升级,预算如何分配?',     navContrast: 'normal' },
  { pc: imgHome2_PC,  tablet: imgHome2_T,  mobile: imgHome2_M,  message: '家装风格要兼顾颜值与实用?', navContrast: 'high' },
  { pc: imgStore3_PC, tablet: imgStore3_T, mobile: imgStore3_M, message: '店铺工程需要预算大概多少?',     navContrast: 'high' },
] as const

const pillMessages = computed(() => slides.map((s) => s.message))
const activeIndex = ref(0)
const activeMessageIndex = computed(() => activeIndex.value)
// activeNavContrastMode 已不再使用(nav 全局提到 App.vue),保留 slide.navContrast 字段未来扩展
const firstSlideImage = computed(() => {
  if (typeof window === 'undefined') return slides[0]?.pc ?? ''
  if (window.matchMedia('(max-width: 768px)').matches) return slides[0]?.mobile ?? ''
  if (window.matchMedia('(max-width: 1024px)').matches) return slides[0]?.tablet ?? ''
  return slides[0]?.pc ?? ''
})

let intervalId: ReturnType<typeof setInterval> | undefined

function advanceSlide() { activeIndex.value = (activeIndex.value + 1) % slides.length }
function startAutoPlay() {
  if (intervalId !== undefined || slides.length <= 1) return
  intervalId = setInterval(advanceSlide, HERO_CAROUSEL_INTERVAL_MS)
}
function stopAutoPlay() {
  if (intervalId !== undefined) { clearInterval(intervalId); intervalId = undefined }
}
function onVisibilityChange() {
  if (typeof document === 'undefined') return
  document.hidden ? stopAutoPlay() : startAutoPlay()
}

// 非首屏图懒加载 — 防止 6 张图并发挤压首图带宽
const loadedIndices = ref<number[]>([0])

function getSlideStyle(i: number, slide: HeroSlide): Record<string, string> {
  if (!loadedIndices.value.includes(i)) return {}
  return {
    '--img-pc': `url(${slide.pc})`,
    '--img-tablet': `url(${slide.tablet})`,
    '--img-mobile': `url(${slide.mobile})`,
  }
}

function pickUrlForViewport(slide: HeroSlide): string {
  if (typeof window === 'undefined') return slide.pc
  if (window.matchMedia('(max-width: 768px)').matches) return slide.mobile
  if (window.matchMedia('(max-width: 1024px)').matches) return slide.tablet
  return slide.pc
}

function preloadSlide(i: number): void {
  if (i >= slides.length) return
  const img = new Image()
  const finish = () => {
    if (!loadedIndices.value.includes(i)) {
      loadedIndices.value = [...loadedIndices.value, i]
    }
    preloadSlide(i + 1)
  }
  img.onload = finish
  img.onerror = finish
  img.src = pickUrlForViewport(slides[i] ?? slides[0]!)
}

function onPillClick() { openChat() }

onMounted(() => {
  if (typeof window === 'undefined') return
  const startLazy = () => preloadSlide(1)
  type RIC = (cb: () => void, opts?: { timeout: number }) => number
  const ric = (window as unknown as { requestIdleCallback?: RIC }).requestIdleCallback
  if (typeof ric === 'function') {
    ric(startLazy, { timeout: 3000 })
  } else {
    setTimeout(startLazy, 1500)
  }
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    startAutoPlay()
  }
  document.addEventListener('visibilitychange', onVisibilityChange)
})

onUnmounted(() => {
  stopAutoPlay()
  if (typeof document !== 'undefined') {
    document.removeEventListener('visibilitychange', onVisibilityChange)
  }
})
</script>

<style scoped>
.hero {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  overflow: hidden;
  background: var(--mk-paper);
  opacity: 0;
  animation: hero-fade 0.55s ease forwards;
}
/* 移动端 hero 高度自适应屏幕:不强制 100dvh,留出下方 stats 一点点露头(用户反馈) */
@media (max-width: 768px) {
  .hero { min-height: clamp(580px, 88dvh, 760px); }
}
@keyframes hero-fade { from { opacity: 0; } to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .hero { opacity: 1; animation: none; } }

/* LQIP 模糊底图:store1 32px webp base64,蓝桃灰大色块过渡 */
.hero-base {
  position: absolute; inset: 0; z-index: 0;
  background-image: url('data:image/webp;base64,UklGRrwAAABXRUJQVlA4ILAAAACwBACdASogABcAPxFyr1AsJqQisAgBgCIJQBg5gv7hBPE988oAqpe69Qyn1U7AAP7jRT3RR7qQ4e0qY4Mr3CoMQVPaHcycELZtqJpdMuYAnCiudS1szq+t205PenKgT59SMT7rckwJhSb6L2GJzjVV44XKyoungIOviueQvRXYdaQ0RYn5Drwx3ilCuXSZkhNCMmBjDQAh7eDAU7FTXwCbiFfK/mXNp2TUlsy6ULjAAA==');
  background-size: cover;
  background-position: center;
  filter: blur(24px);
  transform: scale(1.06);
}

.hero-bg {
  position: absolute; inset: 0; z-index: 1;
  overflow: hidden;
}
.hero-preload {
  position: absolute;
  width: 1px; height: 1px;
  opacity: 0;
  pointer-events: none;
}
.hero-bg-layer {
  position: absolute; inset: 0;
  background-size: cover;
  background-position: center;
  background-image: var(--img-pc);
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.45, 0, 0.2, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  transform: translateZ(0);
}
.hero-bg-layer--active { opacity: 1; }
@media (max-width: 1024px) { .hero-bg-layer { background-image: var(--img-tablet); } }
@media (max-width: 768px)  { .hero-bg-layer { background-image: var(--img-mobile); } }
@media (prefers-reduced-motion: reduce) {
  .hero-bg-layer { transition: none; }
}

/* v2 蒙版(用户反馈持续调优:白色透明度降低,让图片更清晰透过) */
.hero-mask {
  position: absolute; inset: 0; z-index: 2;
  background: linear-gradient(
    180deg,
    rgba(26, 26, 26, 0.38) 0%,
    rgba(26, 26, 26, 0.14) 22%,
    rgba(255, 255, 255, 0.12) 42%,
    rgba(255, 255, 255, 0.28) 62%,
    rgba(245, 242, 236, 0.7) 82%,
    var(--mk-paper) 100%
  );
  pointer-events: none;
}

/* NavigationBar 是 sticky position,会自己浮在顶部 */

/* 主内容居中堆叠 — Z 字标题 + tag + subtitle */
.hero-inner {
  position: relative;
  z-index: 10;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 24px 140px;
  max-width: 1080px;
  margin: 0 auto;
  gap: 28px;
}
/* 移动端:文字定位"中上"(用户反馈) — 从顶部 22dvh 开始,不再垂直居中 */
@media (max-width: 768px) {
  .hero-inner {
    justify-content: flex-start;
    padding: 22dvh 20px 36px;
    gap: 18px;
  }
}

.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 18px;
  font-family: var(--mk-font-serif);
  font-weight: 500;
  font-size: 17px;
  color: rgba(255, 255, 255, 0.96);
  letter-spacing: 0.42em;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 4px;
}
.hero-tag::before, .hero-tag::after {
  content: '';
  width: 56px;
  height: 1px;
  background: rgba(184, 134, 11, 0.85);
}
@media (max-width: 768px) {
  .hero-tag { font-size: 13px; letter-spacing: 0.3em; gap: 12px; }
  .hero-tag::before, .hero-tag::after { width: 32px; }
}

.hero-title {
  margin: 0;
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  font-family: var(--mk-font-serif);
  font-size: clamp(56px, 8vw, 108px);
  font-weight: 600;
  line-height: 1.18;
  letter-spacing: 0.06em;
  color: white;
  text-shadow: 0 8px 28px rgba(0, 0, 0, 0.7);
}
.hero-title__line { display: block; }
/* Z 字结构:第二行向右偏移 ~2 个字符宽度,让"筑"与"心"对齐 */
.hero-title__line--2 {
  padding-left: 2.12em;
}

/* hero-accent 朱红色块去除(用户反馈),保留类名占位以便未来恢复 */
.hero-accent {
  display: inline-block;
  color: white;
}

.hero-subtitle {
  margin: 0;
  font-size: 24px;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 0.2em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
}
@media (max-width: 768px) {
  .hero-subtitle { font-size: 14px; letter-spacing: 0.14em; }
}

/* pill 大致与"凡"字结束位置对齐:
   hero-inner max-width 1080 居中,标题宽约 7.4em(对应 clamp 字号);
   pill 右对齐 + 给右侧留出 "(容器宽 - 标题宽) / 2" 的边距 ≈ clamp(40, 12vw, 200)
   实现:hero-inner padding-right 不变,pill 用 margin-right 把自己往左推 */
.hero-pill-pos {
  align-self: flex-end;
  margin-top: 8px;
  margin-right: clamp(0, 5vw, 60px);
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.2, 0.85, 0.3, 1.05);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  border-radius: 18px;
}
.hero-pill-pos:hover { transform: translateY(-2px); }
.hero-pill-pos:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.7);
  outline-offset: 4px;
  border-radius: 18px;
}
@media (max-width: 768px) {
  .hero-pill-pos { align-self: center; }
}

.hero-scroll-indicator {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--mk-font-serif);
  font-size: 12px;
  letter-spacing: 0.3em;
  color: rgba(26, 26, 26, 0.55);  /* 底部已融入米灰,用深色更易读 */
  z-index: 11;
  animation: hero-scroll-bounce 2.4s ease-in-out infinite;
}
@keyframes hero-scroll-bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(6px); }
}
@media (prefers-reduced-motion: reduce) {
  .hero-scroll-indicator { animation: none; }
}
</style>
