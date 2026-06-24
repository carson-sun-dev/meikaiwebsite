<template>
  <section class="mk-section why-section">
    <div class="mk-container">
      <header class="mk-section-header" ref="headerRef" :class="{ 'is-visible': revealedHeader }">
        <span class="mk-eyebrow">Why Choose Us</span>
        <h2 class="mk-title">为什么选择美恺</h2>
        <p class="mk-title-sub">我们承诺,每一项都做到</p>
      </header>

      <div class="why-grid">
        <article
          v-for="(row, i) in homeWhyItems"
          :key="row.name"
          class="why-card"
          :class="{ 'is-visible': revealedCards }"
          :style="{ transitionDelay: `${i * 0.08}s` }"
        >
          <span class="why-card__num">{{ row.num }}</span>
          <h3 class="why-card__title">{{ row.title }}</h3>
          <p class="why-card__body">{{ row.body }}</p>
        </article>
      </div>
    </div>
  </section>
  <!-- 按用户决策:Why 节区**不带**尾部 divider -->
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { homeWhyItems } from '@/data/homeWhyItems'

const headerRef = ref<HTMLElement | null>(null)
const revealedHeader = ref(false)
const revealedCards = ref(false)

let obs: IntersectionObserver | undefined

onMounted(() => {
  if (typeof window === 'undefined') return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealedHeader.value = true
    revealedCards.value = true
    return
  }
  if (!headerRef.value) return
  obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        revealedHeader.value = true
        // 卡片稍后触发,跟 header 错开
        setTimeout(() => { revealedCards.value = true }, 120)
        obs?.disconnect()
      }
    })
  }, { threshold: 0.15 })
  obs.observe(headerRef.value)
})

onUnmounted(() => obs?.disconnect())
</script>

<style scoped>
.why-section { background: var(--mk-paper-pure); }

.mk-section-header {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.why-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}
@media (max-width: 1200px) { .why-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px)  { .why-grid { grid-template-columns: 1fr; } }

.why-card {
  position: relative;
  background: var(--mk-card);
  padding: 40px 26px;
  border: 1px solid var(--mk-line);
  border-radius: 6px;
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1),
              border-color 0.3s ease, box-shadow 0.3s ease;
}
.why-card.is-visible { opacity: 1; transform: translateY(0); }

.why-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--mk-brand);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s cubic-bezier(0.2, 0.85, 0.3, 1);
}
.why-card:hover {
  border-color: rgba(196, 30, 58, 0.5);
  box-shadow: var(--mk-shadow-md);
  transform: translateY(-6px) !important;
}
.why-card:hover::before { transform: scaleX(1); }

.why-card__num {
  display: block;
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 46px;
  color: var(--mk-gold);
  line-height: 1;
  margin-bottom: 22px;
  opacity: 0.85;
}

.why-card__title {
  font-family: var(--mk-font-serif);
  font-size: 18px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 14px;
  letter-spacing: 0.04em;
  line-height: 1.5;
}

.why-card__body {
  margin: 0;
  font-size: 13.5px;
  color: var(--mk-ink-3);
  line-height: 1.8;
}

@media (prefers-reduced-motion: reduce) {
  .why-card { opacity: 1; transform: none !important; transition: none; }
  .why-card:hover { transform: none !important; }
}

/* 触摸屏:卡片顶部红条 + 边框朱红 直接激活,不再依赖 hover */
@media (hover: none) and (pointer: coarse) {
  .why-card { border-color: rgba(196, 30, 58, 0.28); }
  .why-card::before { transform: scaleX(1); }
  .why-card:hover { transform: none !important; }
}
</style>
