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
      <NavigationBar />

      <h1 class="hero-frame6">
        <div class="hero-frame5">
          <span class="hero-title-first hero-title-display">以匠心</span>
          <HeroQuoteSearchPill :messages="pillMessages" :active-index="activeMessageIndex" @search="onQuoteSearchClick" />
        </div>
        <span class="hero-title-second hero-title-display">筑非凡</span>
      </h1>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

import NavigationBar from '@/components/navigationBar.vue'
import imgStore1 from '@/source/homepage/1/store1.jpg'
import imgStore2 from '@/source/homepage/1/store2.jpg'

import HeroQuoteSearchPill from './HeroQuoteSearchPill.vue'

/** 背景与玻璃条文案同一时刻切换（同一 interval tick） */
const HERO_CAROUSEL_INTERVAL_MS = 5500

const emit = defineEmits<{
  quoteSearch: []
}>()

const heroImages = [imgStore1, imgStore2] as const

/** 占位文案，后续可抽成常量或 props */
const pillMessages = [
  '我的店铺装修报价是？',
  '办公室翻新·免费出方案',
  '金水区门店·预约量房设计',
] as const

/** 每次 tick 同时推进：用于背景与文案 */
const step = ref(0)

const activeImageIndex = computed(() => step.value % heroImages.length)
const activeMessageIndex = computed(() => step.value % pillMessages.length)

let intervalId: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return
  }
  intervalId = setInterval(() => {
    step.value += 1
  }, HERO_CAROUSEL_INTERVAL_MS)
})

onUnmounted(() => {
  if (intervalId !== undefined) {
    clearInterval(intervalId)
  }
})

function onQuoteSearchClick() {
  emit('quoteSearch')
}
</script>

<style scoped>
.hero-section {
  position: relative;
  display: flex;
  min-height: 100dvh;
  flex-direction: column;
  overflow: hidden;
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
    'PingFang SC',
    'Hiragino Sans GB',
    'Microsoft YaHei',
    sans-serif;
  font-size: clamp(2.5rem, 7.5vw + 1rem, 5.5rem);
  font-weight: 900;
  font-style: normal;
  line-height: 1.08;
  letter-spacing: 0.02em;
  color: rgba(255, 255, 255, 0.96);
  -webkit-font-smoothing: antialiased;
  text-shadow:
    0 2px 28px rgb(0 0 0 / 0.5),
    0 1px 3px rgb(0 0 0 / 0.4);
}

.hero-frame6 {
  display: flex;
  width: 100%;
  max-width: 940px;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  gap: 6px;
  margin-top: auto;
}

.hero-frame5 {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 16px;
  margin: 0;
}

.hero-title-first {
  flex: 1 1 0;
  min-width: 0;
}

.hero-title-second {
  display: block;
  width: 100%;
  max-width: 940px;
  margin: 0;
  text-align: center;
}

@media (max-width: 900px) {
  .hero-frame5 {
    flex-direction: column;
    align-items: stretch;
  }

  .hero-title-first {
    text-align: left;
  }

  .hero-frame6 {
    align-items: stretch;
  }
}
</style>
