<template>
  <section class="hero-section">
    <div class="hero-base" aria-hidden="true" />

    <div class="hero-bg" aria-hidden="true">
      <div
        v-for="(img, i) in heroImages"
        :key="`hero-bg-${i}`"
        class="hero-bg-layer"
        :class="{ 'hero-bg-layer--active': i === activeImageIndex }"
        :style="{ backgroundImage: `url(${img})` }"
      />
    </div>

    <div class="hero-overlay" />

    <div class="hero-shell">
      <NavigationBar :contrast-mode="activeNavContrastMode" />

      <h1 class="hero-frame6">
        <div class="hero-pill">
          <HeroQuoteSearchPill
            :messages="pillMessages"
            :active-index="activeMessageIndex"
            @search="onQuoteSearchClick"
          />
        </div>
        <span class="hero-title-first hero-title-display">以匠心</span>
        <span class="hero-title-second hero-title-display">筑非凡</span>
      </h1>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

import NavigationBar from '@/components/navigationBar.vue'
import imgBusiness1 from '@/source/homepage/1/bussiness1.jpg'
import imgBusiness3 from '@/source/homepage/1/bussiness3.jpg'
import imgHome1 from '@/source/homepage/1/home1.jpg'
import imgHome2 from '@/source/homepage/1/home2.jpg'
import imgStore1 from '@/source/homepage/1/store1.jpg'
import imgStore2 from '@/source/homepage/1/store2.jpg'
import imgStore3 from '@/source/homepage/1/store3.jpg'

import HeroQuoteSearchPill from './HeroQuoteSearchPill.vue'

/** 背景与玻璃条文案同一时刻切换（同一 tick） */
const HERO_CAROUSEL_INTERVAL_MS = 4000

const emit = defineEmits<{
  quoteSearch: [targetRoute: string]
}>()

type HeroSlide = {
  image: string
  message: string
  navContrast: 'normal' | 'high'
  route: '/store' | '/business' | '/residential'
}

/**
 * 固定播放顺序：
 * 店铺 -> 商务 -> 家装，然后继续循环
 */
const slides: readonly HeroSlide[] = [
  { image: imgStore1, message: '店铺改造不歇业，施工能否分阶段？', navContrast: 'high', route: '/store' },
  { image: imgBusiness1, message: '商务办公翻新，如何高效落地？', navContrast: 'normal', route: '/business' },
  { image: imgHome1, message: '家装设计施工，多久可以入住？', navContrast: 'high', route: '/residential' },
  { image: imgStore2, message: '店铺装饰风格怎么做更吸引顾客？', navContrast: 'high', route: '/store' },
  { image: imgBusiness3, message: '办公空间升级，预算如何分配更合理？', navContrast: 'normal', route: '/business' },
  { image: imgHome2, message: '家装风格落地，怎样兼顾颜值与实用？', navContrast: 'high', route: '/residential' },
  { image: imgStore3, message: '我的店铺工程需要预算大概多少？', navContrast: 'high', route: '/store' },
] as const

const heroImages = computed(() => slides.map((slide) => slide.image))
const pillMessages = computed(() => slides.map((slide) => slide.message))

const activeIndex = ref(0)
const activeImageIndex = computed(() => activeIndex.value)
const activeMessageIndex = computed(() => activeIndex.value)
const activeNavContrastMode = computed(() => slides[activeIndex.value]?.navContrast ?? 'normal')

let intervalId: ReturnType<typeof setInterval> | undefined

function advanceSlide() {
  activeIndex.value = (activeIndex.value + 1) % slides.length
}

function startAutoPlay() {
  if (intervalId !== undefined || slides.length <= 1) {
    return
  }
  intervalId = setInterval(advanceSlide, HERO_CAROUSEL_INTERVAL_MS)
}

function stopAutoPlay() {
  if (intervalId !== undefined) {
    clearInterval(intervalId)
    intervalId = undefined
  }
}

function onVisibilityChange() {
  if (typeof document === 'undefined') {
    return
  }
  if (document.hidden) {
    stopAutoPlay()
    return
  }
  startAutoPlay()
}

onMounted(() => {
  if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return
  }
  startAutoPlay()
  if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', onVisibilityChange)
  }
})

onUnmounted(() => {
  stopAutoPlay()
  if (typeof document !== 'undefined') {
    document.removeEventListener('visibilitychange', onVisibilityChange)
  }
})

function onQuoteSearchClick() {
  emit('quoteSearch', slides[activeIndex.value]?.route ?? '/store')
}
</script>

<style scoped>
.hero-section {
  position: relative;
  display: flex;
  min-height: 100dvh;
  flex-direction: column;
  overflow: hidden;
  opacity: 0;
  animation: hero-section-fade 0.55s ease forwards;
}

.hero-base {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: #6a6a6a;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 1;
  overflow: hidden;
}

.hero-bg-layer {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.45, 0, 0.2, 1);
}

.hero-bg-layer--active {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .hero-bg-layer {
    transition: none;
  }

  .hero-bg-layer--active {
    opacity: 1;
  }

  .hero-bg-layer:not(.hero-bg-layer--active) {
    opacity: 0;
  }
}

.hero-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  background: rgba(0, 0, 0, 0.28);
}

.hero-shell {
  position: relative;
  z-index: 10;
  display: flex;
  width: 100%;
  min-height: 100dvh;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 110px;
  box-sizing: border-box;
}

/* 主标语：简体优先、偏豪放的窄黑（Noto Sans SC Heavy） */
.hero-title-display {
  font-family:
    'Noto Sans SC',
    'Alibaba PuHuiTi',
    'Source Han Sans SC',
    'PingFang SC',
    'Hiragino Sans GB',
    'Microsoft YaHei',
    sans-serif;
  font-size: clamp(2.85rem, 8.2vw + 1rem, 6.1rem);
  font-weight: 900;
  font-style: normal;
  line-height: 1.06;
  letter-spacing: 0.01em;
  color: rgba(255, 255, 255, 0.88);
  -webkit-font-smoothing: antialiased;
  text-shadow:
    0 3px 34px rgb(0 0 0 / 0.58),
    0 1px 4px rgb(0 0 0 / 0.45);
}

/* 桌面：第一行「以匠心 | 玻璃条」，第二行「筑非凡」居中 */
.hero-frame6 {
  display: grid;
  width: 100%;
  max-width: 940px;
  margin-top: auto;
  grid-template-columns: minmax(0, 1fr) auto;
  grid-template-rows: auto auto;
  align-items: center;
  column-gap: 16px;
  row-gap: 6px;
}

.hero-pill {
  grid-column: 2;
  grid-row: 1;
  justify-self: end;
  display: flex;
  justify-content: flex-end;
  min-width: 0;
}

.hero-title-first {
  grid-column: 1;
  grid-row: 1;
  min-width: 0;
  margin: 0;
  font-size: clamp(3.25rem, 9.2vw + 1rem, 6.85rem);
  transform: skewX(-3deg);
}

.hero-title-second {
  grid-column: 1 / -1;
  grid-row: 2;
  margin: 0;
  text-align: center;
  transform: skewX(-3deg);
}

@media (max-width: 900px) {
  .hero-shell {
    padding: 16px 16px 96px;
  }

  /* 平板/手机：三行 — 玻璃条靠左、以匠心靠左、筑非凡靠右 */
  .hero-frame6 {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    justify-items: start;
    align-items: start;
    row-gap: 10px;
  }

  .hero-pill {
    grid-column: 1;
    grid-row: 1;
    justify-self: start;
    justify-content: flex-start;
  }

  .hero-title-first {
    grid-column: 1;
    grid-row: 2;
    width: auto;
    text-align: left;
    justify-self: start;
  }

  .hero-title-second {
    grid-column: 1;
    grid-row: 3;
    width: 100%;
    justify-self: stretch;
    text-align: right;
    line-height: 1.05;
  }
}

@media (max-width: 480px) {
  .hero-shell {
    padding: 12px 12px 80px;
  }
}

@keyframes hero-section-fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-section {
    opacity: 1;
    animation: none;
  }
}
</style>
