<template>
  <section class="mk-section ci-section">
    <div class="mk-container ci-grid">
      <div class="ci-text" :class="{ 'is-visible': revealed }" ref="textRef">
        <span class="mk-eyebrow">About Meikai</span>
        <h2 class="mk-title">关于美恺</h2>
        <p class="ci-lead">
          多年深耕，美恺以丰富的装饰经验为基石，<span class="ci-accent">致力于为您破解空间难题</span>。
        </p>
        <p class="ci-para">
          用匠心构筑品质环境，以卓越空间助力您的事业成功。始创于 {{ foundedYear }} 年，以郑州为核心辐射河南全省；我们始终以客户意见为导向，筑造中原高品质装饰标杆。
        </p>
        <p class="ci-para">
          总工领衔 30 年行业经验，坚持一对一深度对接。凭借卓越的施工速度与交付质量，在河南市场赢得深厚口碑认证——多家河南知名企业合作伙伴，工程质量广受好评。
        </p>
        <!-- v2 demo signature 块:替代原"了解企业历程"按钮(用户反馈) -->
        <div class="ci-signature">
          <div class="ci-signature__line">· 美恺装饰 ·</div>
          <div class="ci-signature__name">郑州 · 河南全省</div>
        </div>
      </div>

      <div class="ci-img-wrap" :class="{ 'is-visible': revealed }">
        <div class="ci-img" :style="{ backgroundImage: `url(${aboutImg})` }" aria-hidden="true"></div>
        <div class="ci-img-badge">
          <div class="ci-img-badge-num">{{ years }}</div>
          <div class="ci-img-badge-label">YEARS</div>
        </div>
      </div>
    </div>
    <!-- Stats 已抽出为 HomeStatsSection 紧贴 Hero 下方(用户反馈) -->
  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import aboutImg from '@/source/homepage/3/典雅客厅.webp'
import { COMPANY_FOUNDED_YEAR, getYearsSinceFoundedInclusive } from '@/utils/companyTimeline'

const foundedYear = COMPANY_FOUNDED_YEAR
const years = getYearsSinceFoundedInclusive()

const textRef = ref<HTMLElement | null>(null)
const revealed = ref(false)

let textObs: IntersectionObserver | undefined

onMounted(() => {
  if (typeof window === 'undefined') return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) {
    revealed.value = true
    return
  }
  if (!textRef.value) return
  textObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        revealed.value = true
        textObs?.disconnect()
      }
    })
  }, { threshold: 0.15 })
  textObs.observe(textRef.value)
})

onUnmounted(() => {
  textObs?.disconnect()
})
</script>

<style scoped>
.ci-section { background: var(--mk-paper); }

.ci-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 80px;
  align-items: center;
}
@media (max-width: 1024px) {
  .ci-grid { grid-template-columns: 1fr; gap: 56px; }
}

.ci-text {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.ci-text.is-visible { opacity: 1; transform: translateY(0); }

.ci-text .mk-eyebrow { display: block; }
.ci-text .mk-title { display: block; margin-bottom: 28px; }

.ci-lead {
  font-family: var(--mk-font-serif);
  font-size: 22px;
  color: var(--mk-ink);
  line-height: 1.7;
  letter-spacing: 0.04em;
  margin: 0 0 22px;
}
.ci-accent { color: var(--mk-brand); }

.ci-para {
  color: var(--mk-ink-2);
  font-size: 15px;
  line-height: 1.95;
  letter-spacing: 0.03em;
  margin: 0 0 18px;
}

/* v2 signature 块(替代原"了解企业历程"按钮) */
.ci-signature {
  margin-top: 32px;
  display: inline-flex;
  flex-direction: column;
  padding: 14px 24px;
  border-left: 2px solid var(--mk-brand);
  background: var(--mk-card);
  border-radius: 0 4px 4px 0;
  box-shadow: var(--mk-shadow-sm);
}
.ci-signature__line {
  font-size: 13px;
  color: var(--mk-ink-3);
  letter-spacing: 0.18em;
  font-family: var(--mk-font-en);
  /* font-style: italic; */
}
.ci-signature__name {
  font-family: var(--mk-font-serif);
  font-size: 18px;
  color: var(--mk-ink);
  margin-top: 6px;
  letter-spacing: 0.1em;
  font-weight: 500;
}

/* 右图 */
.ci-img-wrap {
  position: relative;
  aspect-ratio: 4 / 5;
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) 0.15s,
              transform 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) 0.15s;
}
.ci-img-wrap.is-visible { opacity: 1; transform: translateY(0); }

.ci-img {
  position: absolute;
  inset: 0;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  border-radius: 4px;
}
.ci-img-wrap::before {
  content: '';
  position: absolute;
  top: -16px; left: -16px;
  right: 16px; bottom: 16px;
  border: 1px solid var(--mk-gold);
  z-index: -1;
  border-radius: 4px;
}
.ci-img-badge {
  position: absolute;
  bottom: 24px; left: 24px;
  background: var(--mk-brand);
  color: white;
  padding: 18px 28px;
  font-family: var(--mk-font-serif);
  border-radius: 2px;
}
.ci-img-badge-num { font-size: 36px; line-height: 1; }
.ci-img-badge-label {
  font-size: 12px;
  letter-spacing: 0.3em;
  margin-top: 6px;
  opacity: 0.9;
  font-family: var(--mk-font-en);
  /* font-style: italic; */
}

/* Stats 已抽出为 HomeStatsSection,本组件不再含 */
</style>
