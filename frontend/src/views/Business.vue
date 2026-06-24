<template>
  <div class="inner-page">
    <!-- NavigationBar 全局在 App.vue,本页面不再重复 -->

    <!-- Hero:单图 + v2 蒙版 + 居中宋体标题(占满首屏 100dvh) -->
    <section class="inner-hero" :style="{ backgroundImage: `url(${heroImg})` }">
      <div class="inner-hero__mask" aria-hidden="true"></div>
      <div class="inner-hero__inner">
        <div class="inner-hero__tag">商 务 · 办 公 空 间</div>
        <h1 class="inner-hero__title">兼顾<span class="accent">效率</span>与<span class="accent">品牌感</span></h1>
        <p class="inner-hero__sub">
          围绕协作效率、员工体验与企业形象,提供从规划设计到工程交付的一体化服务
        </p>
        <!-- 用户反馈:hero 不再放 CTA 按钮,引流意图统一由全局右下 ChatFab 承接 -->
      </div>
    </section>

    <!-- Highlights -->
    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi1" :class="{ 'is-visible': v1 }">
          <span class="mk-eyebrow">Why Enterprises</span>
          <h2 class="mk-title">为什么企业客户选择我们</h2>
        </header>
        <div class="inner-grid-3">
          <article
            v-for="(item, i) in highlights"
            :key="item.title"
            class="inner-card"
            :class="{ 'is-visible': v1 }"
            :style="{ transitionDelay: `${i * 0.1}s` }"
          >
            <span class="inner-card__num">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3 class="inner-card__title">{{ item.title }}</h3>
            <p class="inner-card__text">{{ item.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
      <span class="mk-divider__seal"></span>
    </div>

    <!-- Process -->
    <section class="mk-section inner-section inner-section--alt">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi2" :class="{ 'is-visible': v2 }">
          <span class="mk-eyebrow">Our Process</span>
          <h2 class="mk-title">办公项目服务流程</h2>
        </header>
        <div class="inner-process">
          <div
            v-for="(step, idx) in processSteps"
            :key="step.title"
            class="inner-step"
            :class="{ 'is-visible': v2 }"
            :style="{ transitionDelay: `${idx * 0.1}s` }"
          >
            <div class="inner-step__num">{{ ['壹','贰','叁'][idx] }}</div>
            <h3 class="inner-step__title">{{ step.title }}</h3>
            <p class="inner-step__desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
      <span class="mk-divider__seal"></span>
    </div>

    <!-- Cases -->
    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi4" :class="{ 'is-visible': v4 }">
          <span class="mk-eyebrow">Selected Cases</span>
          <h2 class="mk-title">商务办公案例</h2>
        </header>
        <div class="inner-case-grid">
          <article
            v-for="(item, i) in cases"
            :key="item.title"
            class="inner-case"
            :class="{ 'is-visible': v4 }"
            :style="{ transitionDelay: `${i * 0.08}s` }"
          >
            <div class="inner-case__media">
              <img :src="item.imageA" alt="" class="inner-case__img" />
              <img :src="item.imageB" alt="" class="inner-case__img" />
            </div>
            <div class="inner-case__body">
              <h3 class="inner-case__title">{{ item.title }}</h3>
              <div class="inner-case__meta">
                <span>{{ item.type }}</span>
                <span>·</span>
                <span>{{ item.area }}</span>
                <span>·</span>
                <span>{{ item.duration }}</span>
              </div>
              <p class="inner-case__desc">{{ item.desc }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
      <span class="mk-divider__seal"></span>
    </div>

    <!-- Pricing 区间 — 移到 Cases 之后(用户反馈) -->
    <section class="mk-section inner-section inner-section--alt">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi3" :class="{ 'is-visible': v3 }">
          <span class="mk-eyebrow">Price Range</span>
          <h2 class="mk-title">报价区间参考</h2>
          <p class="mk-title-sub">仅供参考  ·  精确报价以现场量房为准</p>
        </header>
        <div class="inner-grid-3">
          <article
            v-for="(item, i) in priceBands"
            :key="item.label"
            class="inner-price-card"
            :class="{ 'is-visible': v3 }"
            :style="{ transitionDelay: `${i * 0.1}s` }"
          >
            <p class="inner-price-card__label">{{ item.label }}</p>
            <p class="inner-price-card__range">{{ item.range }}</p>
            <div class="inner-price-card__divider"></div>
            <p class="inner-price-card__hint">{{ item.hint }}</p>
          </article>
        </div>
      </div>
    </section>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import HomeFooter from '@/components/home/HomeFooter.vue'
import { useChatWidget } from '@/composables/useChatWidget'

const { open: openChat } = useChatWidget()
import logoImg from '@/source/logo/logo.webp'
import heroImg from '@/source/business/biz1.webp'   // 新 unsplash 高质图当 hero

import biz1 from '@/source/business/biz1.webp'
import biz2 from '@/source/business/biz2.webp'
import biz3 from '@/source/business/biz3.webp'
import biz4 from '@/source/business/biz4.webp'
import biz5 from '@/source/business/biz5.webp'

// 副图:用旧 b 系列凑双图布局(临时,待店主提供原图后替换)
import bAlt1 from '@/source/business/b1_2.webp'
import bAlt2 from '@/source/business/b2_1.webp'
import bAlt3 from '@/source/business/b2_2.webp'
import bAlt4 from '@/source/business/b3_1.webp'
import bAlt5 from '@/source/business/b3_2.webp'

const highlights = [
  { title: '效率导向布局', text: '围绕部门协作和会议频次规划空间,减少无效跑动,提升团队沟通效率。' },
  { title: '企业形象统一', text: '前台、会客区、开放办公与文化墙风格统一,强化品牌识别与客户第一印象。' },
  { title: '工期与成本可控', text: '节点化管理施工流程,预算按分项透明拆解,降低追加和延期风险。' },
] as const

const processSteps = [
  { title: '需求调研与办公诊断', desc: '了解团队规模、岗位协同和未来扩编计划,明确功能分区与空间优先级。' },
  { title: '平面优化与预算确认', desc: '深度优化办公区域与工位排布,明码标价、绝无隐形消费的预算方案。' },
  { title: '施工管理与交付培训', desc: '按节点推进施工及验收,完成交付后提供空间使用与维护建议。' },
] as const

const priceBands = [
  { label: '标准办公', range: '¥400 - ¥700 / m²', hint: '适合中小企业基础升级,优先保证工位效率与会议功能。' },
  { label: '形象升级', range: '¥700 - ¥1000 / m²', hint: '适合注重品牌展示和员工体验的成长型团队。' },
  { label: '总部定制', range: '¥1000+ / m²', hint: '适合总部或综合办公空间,强调品牌表达和高品质细节。' },
] as const

// 5 个 case 双图卡:主图用 biz1-5 新 unsplash 高质,副图用旧 b 系列凑补
const cases = [
  // {
  //   title: '科技服务企业 · 开放办公与协作区',
  //   imageA: biz1, imageB: bAlt1,
  //   type: '开放办公', area: '约 380㎡', duration: '工期 52 天',
  //   desc: '工位区与协作区一体化布局,照明与声学处理兼顾专注与讨论,动线缩短跨部门沟通成本。',
  // },
  {
    title: '品牌咨询公司 · 接待与会议空间',
    imageA: biz2, imageB: bAlt2,
    type: '形象办公', area: '约 290㎡', duration: '工期 53 天',
    desc: '前台形象墙与访客串联会议室,材质与灯光统一品牌色,提升客户到访第一印象。',
  },
  {
    title: '区域总部 · 高管办公与茶歇区',
    imageA: biz3, imageB: bAlt3,
    type: '总部办公', area: '约 510㎡', duration: '工期 63 天',
    desc: '独立办公室与共享茶歇区相邻布置,既保证决策私密性,又便于管理层与团队快速对齐。',
  },
  {
    title: '成长型团队 · 联合办公改造',
    imageA: biz4, imageB: bAlt4,
    type: '办公升级', area: '约 220㎡', duration: '工期 44 天',
    desc: '在有限面积内重构储物与工位比例,增设电话间与站立会议角,满足扩编前弹性使用。',
  },
  {
    title: '创业孵化器 · 多功能共享空间',
    imageA: biz5, imageB: bAlt5,
    type: '共享办公', area: '约 460㎡', duration: '工期 58 天',
    desc: '路演区、独立工位与会议室复合使用,可移动家具适配团队规模快速变化。',
  },
] as const

const hi1 = ref<HTMLElement | null>(null)
const hi2 = ref<HTMLElement | null>(null)
const hi3 = ref<HTMLElement | null>(null)
const hi4 = ref<HTMLElement | null>(null)
const v1 = ref(false); const v2 = ref(false); const v3 = ref(false); const v4 = ref(false)
const observers: IntersectionObserver[] = []

function observe(el: HTMLElement | null, flag: { value: boolean }) {
  if (!el) return
  const o = new IntersectionObserver(es => {
    es.forEach(e => {
      if (e.isIntersecting) { flag.value = true; o.disconnect() }
    })
  }, { threshold: 0.15 })
  o.observe(el)
  observers.push(o)
}

onMounted(() => {
  if (typeof window === 'undefined') return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    v1.value = v2.value = v3.value = v4.value = true
    return
  }
  observe(hi1.value, v1); observe(hi2.value, v2); observe(hi3.value, v3); observe(hi4.value, v4)
})
onUnmounted(() => { observers.forEach(o => o.disconnect()) })
</script>

<style scoped>
.inner-page {
  min-height: 100dvh;
  background: var(--mk-paper);
  color: var(--mk-ink);
  font-family: var(--mk-font-sans);
}

/* ============ Hero ============ */
/* .inner-hero* 样式已统一由全局 home-page.css 提供(含 mobile padding/高度自适应),
 * 本页面 scoped 备份已删,避免覆盖全局规则导致移动端调整不生效 */

/* ============ Sections ============ */
.inner-section { background: var(--mk-paper); }
.inner-section--alt { background: var(--mk-paper-pure); }

.mk-section-header {
  text-align: center;
  margin-bottom: 56px;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.inner-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
@media (max-width: 900px) { .inner-grid-3 { grid-template-columns: 1fr; } }

/* Highlights / Why cards */
.inner-card {
  position: relative;
  background: var(--mk-card);
  padding: 38px 28px;
  border: 1px solid var(--mk-line);
  border-radius: 6px;
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1),
              border-color 0.3s ease, box-shadow 0.3s ease;
}
.inner-card.is-visible { opacity: 1; transform: translateY(0); }
.inner-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--mk-brand); transform: scaleX(0); transform-origin: left;
  transition: transform 0.4s ease;
}
.inner-card:hover { border-color: rgba(196, 30, 58, 0.45); box-shadow: var(--mk-shadow-md); transform: translateY(-4px) !important; }
.inner-card:hover::before { transform: scaleX(1); }
.inner-card__num {
  display: block;
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 44px;
  color: var(--mk-gold);
  line-height: 1;
  margin-bottom: 20px;
  opacity: 0.85;
}
.inner-card__title {
  font-family: var(--mk-font-serif);
  font-size: 20px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 12px;
  letter-spacing: 0.05em;
}
.inner-card__text {
  margin: 0;
  font-size: 14px;
  color: var(--mk-ink-3);
  line-height: 1.8;
}

/* Process */
.inner-process {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  position: relative;
}
.inner-process::before {
  content: ''; position: absolute;
  top: 38px; left: 14%; right: 14%;
  height: 1px; background: var(--mk-gold-soft);
}
@media (max-width: 900px) {
  .inner-process { grid-template-columns: 1fr; gap: 32px; }
  .inner-process::before { display: none; }
}
.inner-step {
  text-align: center;
  padding: 0 16px;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.7s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.inner-step.is-visible { opacity: 1; transform: translateY(0); }
.inner-step__num {
  width: 76px; height: 76px;
  margin: 0 auto 22px;
  background: var(--mk-card);
  border: 2px solid var(--mk-brand);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mk-font-serif);
  font-size: 30px; color: var(--mk-brand);
  transition: all 0.4s cubic-bezier(0.2, 0.85, 0.3, 1.05);
}
.inner-step:hover .inner-step__num {
  background: var(--mk-brand); color: white;
  transform: scale(1.08);
}
.inner-step__title {
  font-family: var(--mk-font-serif);
  font-size: 18px; font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 10px;
  letter-spacing: 0.06em;
}
.inner-step__desc {
  margin: 0;
  font-size: 13px;
  color: var(--mk-ink-3);
  line-height: 1.75;
}

/* Pricing */
.inner-price-card {
  background: var(--mk-card);
  border: 1px solid var(--mk-line);
  border-radius: 8px;
  padding: 36px 28px;
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1),
              border-color 0.3s ease, box-shadow 0.3s ease;
}
.inner-price-card.is-visible { opacity: 1; transform: translateY(0); }
.inner-price-card:hover { border-color: rgba(196, 30, 58, 0.45); box-shadow: var(--mk-shadow-md); transform: translateY(-4px) !important; }
.inner-price-card__label {
  margin: 0;
  font-family: var(--mk-font-serif);
  font-size: 17px;
  color: var(--mk-ink-2);
  letter-spacing: 0.1em;
}
.inner-price-card__range {
  margin: 12px 0 0;
  font-family: var(--mk-font-serif);
  font-size: 30px;
  font-weight: 600;
  color: var(--mk-brand);
  letter-spacing: 0.02em;
}
.inner-price-card__divider {
  margin: 18px 0;
  height: 1px;
  background: var(--mk-gold-soft);
}
.inner-price-card__hint {
  margin: 0;
  font-size: 13.5px;
  color: var(--mk-ink-3);
  line-height: 1.8;
}

/* Cases */
.inner-case-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
@media (max-width: 900px) { .inner-case-grid { grid-template-columns: 1fr; } }
.inner-case {
  background: var(--mk-card);
  border: 1px solid var(--mk-line);
  border-radius: 8px;
  overflow: hidden;
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.inner-case.is-visible { opacity: 1; transform: translateY(0); }
.inner-case__media {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}
.inner-case__img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}
.inner-case__body { padding: 28px 28px 32px; }
.inner-case__title {
  font-family: var(--mk-font-serif);
  font-size: 20px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 12px;
  letter-spacing: 0.04em;
}
.inner-case__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 13px;
  color: var(--mk-gold);
  letter-spacing: 0.05em;
  margin-bottom: 14px;
}
.inner-case__desc {
  margin: 0;
  font-size: 14px;
  color: var(--mk-ink-3);
  line-height: 1.85;
}

@media (prefers-reduced-motion: reduce) {
  .inner-card, .inner-step, .inner-price-card, .inner-case {
    opacity: 1; transform: none !important; transition: none;
  }
  .inner-card:hover, .inner-step:hover, .inner-price-card:hover, .inner-case:hover {
    transform: none !important;
  }
}
</style>
