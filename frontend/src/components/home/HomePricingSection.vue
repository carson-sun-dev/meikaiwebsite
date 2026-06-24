<template>
  <section class="mk-section pricing-section">
    <div class="mk-container">
      <header class="mk-section-header" ref="headerRef" :class="{ 'is-visible': revealedHeader }">
        <span class="mk-eyebrow">Pricing</span>
        <h2 class="mk-title">装修参考单价</h2>
        <p class="mk-title-sub">仅供参考  ·  精确报价请联系客服</p>
      </header>

      <div class="pricing-grid">
        <article
          v-for="(plan, i) in plans"
          :key="plan.title"
          class="price-card"
          :class="{ 'is-visible': revealedCards }"
          :style="{ transitionDelay: `${i * 0.1}s` }"
        >
          <h3 class="price-card__title">{{ plan.title }}</h3>
          <div class="price-card__price">
            <span class="price-card__price-num">{{ extractPrice(plan.price) }}</span>
            <span class="price-card__price-unit">￥/m²</span>
          </div>
          <ul class="price-card__list">
            <li v-for="line in plan.lines" :key="line" class="price-card__item">
              <span class="price-card__dot" aria-hidden="true"></span>
              <span>{{ line }}</span>
            </li>
          </ul>
          <router-link
            v-if="props.showDetailButton"
            :to="getPlanDetailRoute(plan.title)"
            class="mk-btn mk-btn--outline price-card__btn"
          >
            了解详情 
          </router-link>
        </article>
      </div>

      <p class="pricing-note">*该单价仅供参考,详情请致电咨询</p>
    </div>
  </section>
  <!-- 用户反馈:Pricing 尾部不带 divider(因后面直接接 Footer,Footer 自带视觉收尾) -->
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import type { HomePricingPlan } from '@/data/homePricingPlans'
import { homePricingPlans } from '@/data/homePricingPlans'
// logoImg 不再需要(divider 已删)

const props = withDefaults(
  defineProps<{
    plans?: HomePricingPlan[]
    showDetailButton?: boolean
  }>(),
  {
    plans: undefined,
    showDetailButton: true,
  },
)

const plans = computed(() => props.plans ?? homePricingPlans)

function getPlanDetailRoute(title: string) {
  if (title.includes('店')) return '/store'
  if (title.includes('商务') || title.includes('办公')) return '/business'
  return '/residential'
}

/** "1200￥/m²" → "1200";其他情况返回原串 */
function extractPrice(price: string): string {
  const m = price.match(/(\d+)/)
  return m?.[1] ?? price
}

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
.pricing-section { background: var(--mk-paper); }

.mk-section-header {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
@media (max-width: 768px) { .pricing-grid { grid-template-columns: 1fr; } }

.price-card {
  display: flex;
  flex-direction: column;
  background: var(--mk-card);
  border: 1px solid var(--mk-line);
  border-radius: 8px;
  padding: 40px 32px 36px;
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1),
              border-color 0.3s ease, box-shadow 0.3s ease;
}
.price-card.is-visible { opacity: 1; transform: translateY(0); }
.price-card:hover {
  transform: translateY(-6px) !important;
  border-color: rgba(196, 30, 58, 0.45);
  box-shadow: var(--mk-shadow-md);
}

.price-card__title {
  font-family: var(--mk-font-serif);
  font-size: 22px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 16px;
  letter-spacing: 0.06em;
}

.price-card__price {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 8px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--mk-gold-soft);
}
.price-card__price-num {
  font-family: var(--mk-font-serif);
  font-size: 46px;
  font-weight: 600;
  color: var(--mk-brand);
  line-height: 1;
}
.price-card__price-unit {
  font-size: 14px;
  color: var(--mk-gold);
  font-family: var(--mk-font-serif);
  letter-spacing: 0.05em;
}

.price-card__list {
  list-style: none;
  margin: 24px 0 0;
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-card__item {
  display: flex;
  gap: 12px;
  font-size: 13.5px;
  color: var(--mk-ink-2);
  line-height: 1.7;
  align-items: flex-start;
}
.price-card__dot {
  margin-top: 8px;
  width: 5px;
  height: 5px;
  flex-shrink: 0;
  background: var(--mk-gold);
  transform: rotate(45deg);
}

.price-card__btn {
  margin-top: 32px;
  align-self: flex-start;
  font-size: 13px;
  padding: 13px 26px;
}

.pricing-note {
  margin-top: 36px;
  text-align: center;
  font-size: 13px;
  color: var(--mk-ink-3);
  letter-spacing: 0.08em;
}

@media (prefers-reduced-motion: reduce) {
  .price-card { opacity: 1; transform: none !important; transition: none; }
  .price-card:hover { transform: none !important; }
}

/* 触摸屏:边框朱红 默认激活,取消 hover 升起避免点击闪烁 */
@media (hover: none) and (pointer: coarse) {
  .price-card { border-color: rgba(196, 30, 58, 0.28); }
  .price-card:hover { transform: none !important; }
}
</style>
