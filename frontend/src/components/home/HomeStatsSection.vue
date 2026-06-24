<template>
  <section class="hero-stats" ref="rootRef" aria-label="美恺装饰核心数据">
    <div class="mk-container">
      <div class="hero-stats__grid">
        <div class="hero-stats__item">
          <div class="hero-stats__num-wrap">
            <span class="hero-stats__num" ref="count1">0</span><span class="hero-stats__unit">年+</span>
          </div>
          <div class="hero-stats__label">深 耕 中 原</div>
        </div>

        <div class="hero-stats__item">
          <div class="hero-stats__num-wrap">
            <span class="hero-stats__num" ref="count2">0</span><span class="hero-stats__unit">+</span>
          </div>
          <div class="hero-stats__label">项 目 交 付</div>
        </div>

        <div class="hero-stats__item">
          <div class="hero-stats__num-wrap">
            <span class="hero-stats__num" ref="count3">0</span><span class="hero-stats__unit">+</span>
          </div>
          <div class="hero-stats__label">工 种 装 修 团 队</div>
        </div>

        <div class="hero-stats__item">
          <div class="hero-stats__num-wrap">
            <span class="hero-stats__num" ref="count4">0</span><span class="hero-stats__unit">%</span>
          </div>
          <div class="hero-stats__label">客 户 满 意 度</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { getYearsSinceFoundedInclusive } from '@/utils/companyTimeline'

const years = getYearsSinceFoundedInclusive()

const rootRef = ref<HTMLElement | null>(null)
const count1 = ref<HTMLElement | null>(null)
const count2 = ref<HTMLElement | null>(null)
const count3 = ref<HTMLElement | null>(null)
const count4 = ref<HTMLElement | null>(null)

let obs: IntersectionObserver | undefined

function animateCount(el: HTMLElement | null, target: number, duration = 1400) {
  if (!el) return
  const start = performance.now()
  const tick = (now: number) => {
    const p = Math.min(1, (now - start) / duration)
    const eased = 1 - Math.pow(1 - p, 3)
    el.textContent = String(Math.round(target * eased))
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

onMounted(() => {
  if (typeof window === 'undefined') return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) {
    if (count1.value) count1.value.textContent = String(years)
    if (count2.value) count2.value.textContent = '350'
    if (count3.value) count3.value.textContent = '30'
    if (count4.value) count4.value.textContent = '96'
    return
  }
  if (!rootRef.value) return
  obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCount(count1.value, years)
        animateCount(count2.value, 350)
        animateCount(count3.value, 30)
        animateCount(count4.value, 96)
        obs?.disconnect()
      }
    })
  }, { threshold: 0.4 })
  obs.observe(rootRef.value)
})

onUnmounted(() => obs?.disconnect())
</script>

<style scoped>
/* 紧贴 hero 下方,无 padding-top 上间距;米灰底 + 暗金细线收边 */
.hero-stats {
  padding: 56px 24px 64px;
  background: var(--mk-paper);
  border-bottom: 1px solid var(--mk-line);
}

.hero-stats__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}
/* ≤900:2x2(用户反馈,不要堆 4 行) */
@media (max-width: 900px) {
  .hero-stats__grid { grid-template-columns: repeat(2, 1fr); gap: 28px 16px; }
}
@media (max-width: 480px) {
  .hero-stats__grid { gap: 24px 12px; }
}

.hero-stats__item {
  text-align: center;
  position: relative;
}
/* 桌面 4 列才显示中间竖线;2x2 不需要(避免错位) */
.hero-stats__item:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 12px; bottom: 12px;
  right: -16px;
  width: 1px;
  background: var(--mk-line);
}
@media (max-width: 900px) {
  .hero-stats__item:not(:last-child)::after { display: none; }
}

.hero-stats__num-wrap {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
}
.hero-stats__num {
  font-family: var(--mk-font-serif);
  font-size: clamp(40px, 5vw, 56px);
  font-weight: 600;
  color: var(--mk-brand);
  line-height: 1;
}
.hero-stats__unit {
  font-size: 18px;
  color: var(--mk-gold);
  font-family: var(--mk-font-serif);
}
.hero-stats__label {
  font-size: 12px;
  color: var(--mk-ink-3);
  margin-top: 12px;
  letter-spacing: 0.32em;
}
</style>
