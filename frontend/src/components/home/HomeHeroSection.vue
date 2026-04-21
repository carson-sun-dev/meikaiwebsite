<template>
  <section class="hero-section">
    <div class="hero-base" aria-hidden="true" />

    <div class="hero-bg" aria-hidden="true">
      <!-- 提高首屏 Hero 首帧加载优先级，降低“文字先出现、背景后到位”的体感 -->
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
        :style="{ 
          '--img-pc': `url(${slide.pc})`, 
          '--img-tablet': `url(${slide.tablet})`, 
          '--img-mobile': `url(${slide.mobile})` 
        }"
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
import HeroQuoteSearchPill from './HeroQuoteSearchPill.vue'

// --- 1. PC 高清版引入 (2560px) ---
import imgBus1_PC from '@/source/homepage/1/pc/bussiness1.webp'
import imgBus3_PC from '@/source/homepage/1/pc/bussiness3.webp'
import imgHome1_PC from '@/source/homepage/1/pc/home1.webp'
import imgHome2_PC from '@/source/homepage/1/pc/home2.webp'
import imgStore1_PC from '@/source/homepage/1/pc/store1.webp'
import imgStore2_PC from '@/source/homepage/1/pc/store2.webp'
import imgStore3_PC from '@/source/homepage/1/pc/store3.webp'

// --- 2. Tablet 平板版引入 (1536px) ---
import imgBus1_T from '@/source/homepage/1/tablet/bussiness1.webp'
import imgBus3_T from '@/source/homepage/1/tablet/bussiness3.webp'
import imgHome1_T from '@/source/homepage/1/tablet/home1.webp'
import imgHome2_T from '@/source/homepage/1/tablet/home2.webp'
import imgStore1_T from '@/source/homepage/1/tablet/store1.webp'
import imgStore2_T from '@/source/homepage/1/tablet/store2.webp'
import imgStore3_T from '@/source/homepage/1/tablet/store3.webp'

// --- 3. Mobile 手机版引入 (1080px) ---
import imgBus1_M from '@/source/homepage/1/mobile/bussiness1.webp'
import imgBus3_M from '@/source/homepage/1/mobile/bussiness3.webp'
import imgHome1_M from '@/source/homepage/1/mobile/home1.webp'
import imgHome2_M from '@/source/homepage/1/mobile/home2.webp'
import imgStore1_M from '@/source/homepage/1/mobile/store1.webp'
import imgStore2_M from '@/source/homepage/1/mobile/store2.webp'
import imgStore3_M from '@/source/homepage/1/mobile/store3.webp'


const HERO_CAROUSEL_INTERVAL_MS = 4000
const emit = defineEmits<{ quoteSearch: [targetRoute: string] }>()

type HeroSlide = {
  pc: string
  tablet: string
  mobile: string
  message: string
  navContrast: 'normal' | 'high'
  route: '/store' | '/business' | '/residential'
}

const slides: readonly HeroSlide[] = [
  { pc: imgStore1_PC, tablet: imgStore1_T, mobile: imgStore1_M, message: '店铺改造不歇业，施工能否分阶段？', navContrast: 'high', route: '/store' },
  { pc: imgBus1_PC, tablet: imgBus1_T, mobile: imgBus1_M, message: '商务办公翻新，如何高效落地？', navContrast: 'normal', route: '/business' },
  { pc: imgHome1_PC, tablet: imgHome1_T, mobile: imgHome1_M, message: '家装设计施工，多久可以入住？', navContrast: 'high', route: '/residential' },
  { pc: imgStore2_PC, tablet: imgStore2_T, mobile: imgStore2_M, message: '店铺装饰风格怎么做更吸引顾客？', navContrast: 'high', route: '/store' },
  { pc: imgBus3_PC, tablet: imgBus3_T, mobile: imgBus3_M, message: '办公空间升级，预算如何分配更合理？', navContrast: 'normal', route: '/business' },
  { pc: imgHome2_PC, tablet: imgHome2_T, mobile: imgHome2_M, message: '家装风格落地，怎样兼顾颜值与实用？', navContrast: 'high', route: '/residential' },
  { pc: imgStore3_PC, tablet: imgStore3_T, mobile: imgStore3_M, message: '我的店铺工程需要预算大概多少？', navContrast: 'high', route: '/store' },
] as const

const pillMessages = computed(() => slides.map((slide) => slide.message))
const activeIndex = ref(0)
const activeMessageIndex = computed(() => activeIndex.value)
const activeNavContrastMode = computed(() => slides[activeIndex.value]?.navContrast ?? 'normal')
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

// 2. 统一生命周期管理
onMounted(() => {
  if (typeof window === 'undefined') return

  // --- 预加载逻辑 ---
  const isMobile = window.matchMedia('(max-width: 768px)').matches
  const isTablet = window.matchMedia('(max-width: 1024px)').matches
  
  slides.slice(0, 2).forEach(slide => {
    const img = new Image()
    img.src = isMobile ? slide.mobile : (isTablet ? slide.tablet : slide.pc)
  })

  // --- 轮播逻辑 ---
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

function onQuoteSearchClick() { emit('quoteSearch', slides[activeIndex.value]?.route ?? '/store') }
</script>

<style scoped>
/* 1. 基础容器与动画 */
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

/* 2. 背景图片层 (分流核心) */
.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 1;
  overflow: hidden;
}

.hero-preload {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.hero-bg-layer {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.45, 0, 0.2, 1);
  
  /* 默认使用 PC 变量 */
  background-image: var(--img-pc);

  /* 硬件加速：防止移动端白屏/闪烁 */
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  transform: translateZ(0);
}

/* 响应式变量切换 */
@media (max-width: 1024px) {
  .hero-bg-layer {
    background-image: var(--img-tablet);
  }
}

@media (max-width: 768px) {
  .hero-bg-layer {
    background-image: var(--img-mobile);
  }
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

/* 3. 内容外壳与文案布局 */
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

.hero-title-display {
  font-family: 'Noto Sans SC', 'Alibaba PuHuiTi', 'Source Han Sans SC', 'PingFang SC', sans-serif;
  font-size: clamp(2.85rem, 8.2vw + 1rem, 6.1rem);
  font-weight: 900;
  line-height: 1.06;
  letter-spacing: 0.01em;
  color: rgba(255, 255, 255, 0.88);
  -webkit-font-smoothing: antialiased;
  text-shadow: 0 3px 34px rgb(0 0 0 / 0.58), 0 1px 4px rgb(0 0 0 / 0.45);
}

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
  display: block;
  grid-column: 1;
  grid-row: 1;
  margin: 0;
  font-size: clamp(3.25rem, 9.2vw + 1rem, 6.85rem);
  transform: skewX(-3deg);
}

.hero-title-second {
  display: block;
  grid-column: 1 / -1;
  grid-row: 2;
  margin: 0;
  width: 100%;
  justify-self: stretch;
  text-align: center;
  transform: skewX(-3deg);
}

/* 4. 移动端 UI 适配 */
@media (max-width: 900px) {
  .hero-shell {
    padding: 16px 16px 96px;
  }
  .hero-frame6 {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    justify-items: start;
    row-gap: 10px;
  }
  .hero-pill {
    grid-column: 1;
    grid-row: 1;
    justify-self: start;
  }
  .hero-title-first {
    grid-column: 1;
    grid-row: 2;
  }
  .hero-title-second {
    grid-column: 1;
    grid-row: 3;
    /* 修复样式丢失关键点： */
    width: 100%;           /* 撑满宽度以便 text-align 生效 */
    text-align: right;     
    line-height: 1.05;
    transform: skewX(-3deg); /* 重新显式声明倾斜 */
    margin-left: 4px;       /* 补偿因倾斜导致的左侧视觉缩进 */
    margin-right: 4rem;
    box-sizing: border-box;
  }
}

@media (max-width: 480px) {
  .hero-shell {
    padding: 12px 12px 80px;
  }
  .hero-title-second {
    margin-left: 2px; /* 窄屏略微缩小补偿 */
  }
}

@keyframes hero-section-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .hero-section {
    opacity: 1;
    animation: none;
  }
}
</style>