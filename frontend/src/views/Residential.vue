<template>
  <div class="inner-page">
    <section class="inner-hero" :style="{ backgroundImage: `url(${heroImg})` }">
      <div class="inner-hero__mask" aria-hidden="true"></div>
      <div class="inner-hero__inner">
        <div class="inner-hero__tag">精 品 · 家 装</div>
        <h1 class="inner-hero__title">打造长期<span class="accent">舒适</span>的<span class="accent">氛围</span></h1>
        <p class="inner-hero__sub">
          从户型评估到软装收尾,以家庭真实使用场景为中心,把"住得舒服"做成可交付的标准
        </p>
      </div>
    </section>

    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi1" :class="{ 'is-visible': v1 }">
          <span class="mk-eyebrow">Why Owners</span>
          <h2 class="mk-title">为什么业主选择我们</h2>
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

    <section class="mk-section inner-section inner-section--alt">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi2" :class="{ 'is-visible': v2 }">
          <span class="mk-eyebrow">Our Process</span>
          <h2 class="mk-title">家装服务流程</h2>
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

    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi4" :class="{ 'is-visible': v4 }">
          <span class="mk-eyebrow">Selected Cases</span>
          <h2 class="mk-title">精品家装案例</h2>
        </header>
        <div class="inner-case-grid">
          <article
            v-for="(item, i) in cases"
            :key="item.title"
            class="inner-case"
            :class="{ 'is-visible': v4 }"
            :style="{ transitionDelay: `${i * 0.06}s` }"
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
import logoImg from '@/source/logo/logo.webp'
import heroImg from '@/source/house/6_2.webp'

import h1a from '@/source/house/1_1.webp'
import h1b from '@/source/house/1_2.webp'
import h2a from '@/source/house/2_1.webp'
import h2b from '@/source/house/2_2.webp'
import h3a from '@/source/homepage/4/1.webp'
import h3b from '@/source/house/3_2.webp'
import h4a from '@/source/house/4_1.webp'
import h4b from '@/source/house/4_2.webp'
import h5a from '@/source/house/5_1.webp'
import h5b from '@/source/house/5_2.webp'
import h6a from '@/source/house/6_1.webp'
import h6b from '@/source/house/6_2.webp'

const highlights = [
  { title: '空间实用优先', text: '从户型评估到收纳设计,以家庭真实使用场景为出发点,让每一处空间都有功能定义。' },
  { title: '风格统一落地', text: '材质、配色、灯光分层规划,效果图与落地一致,避免"图美房子普通"的常见落差。' },
  { title: '施工安心透明', text: '隐蔽工程节点化验收,水电工艺标准化,工长签字 + 监理复核 + 客户复签三重把关。' },
] as const

const processSteps = [
  { title: '户型评估与需求沟通', desc: '结合家庭结构、生活习惯和预算,明确空间改造重点与风格方向。' },
  { title: '方案深化与报价确认', desc: '完成平面规划、收纳系统和材质搭配,并输出分项报价与施工计划。' },
  { title: '施工执行与软装收尾', desc: '分阶段验收施工质量,落地软装与灯光细节,确保入住体验稳定舒适。' },
] as const

const priceBands = [
  { label: '基础家装', range: '¥500 / m²', hint: '适合刚需家庭或出租房升级,优先保证主材安全与基础功能。' },
  { label: '品质居住', range: '¥700 / m²', hint: '适合自住改善型家庭,兼顾设计感与材质升级。' },
  { label: '高端定制', range: '¥900+ / m²', hint: '适合大宅及定制需求,强调整体体验与长期耐用性。' },
] as const

const cases = [
  { title: '奶油风 · 清新简单', imageA: h1a, imageB: h1b, type: '两居新房', area: '约 96㎡', duration: '工期 64 天', desc: '圆弧收口与柔和色系统一全屋,小户型通过镜面与灯光拉伸视觉,兼顾收纳与颜值。' },
  { title: '极简原木 · 亲子家庭', imageA: h2a, imageB: h2b, type: '居住改善', area: '约 106㎡', duration: '工期 71 天', desc: '以木色与留白为主调,儿童房与书房动静分区,收纳嵌入墙体,方便孩子成长阶段调整。' },
  { title: '现代轻奢 · 一体化设计', imageA: h3a, imageB: h3b, type: '平层三居', area: '约 96㎡', duration: '工期 58 天', desc: '打通客餐厅与厨房视线,全屋灯光分层营造温馨而不浮夸的轻奢质感。' },
  { title: '台式简约 · 主卧套间', imageA: h4a, imageB: h4b, type: '套房改造', area: '约 112㎡', duration: '工期 72 天', desc: '主卧与衣帽、梳妆台合并,床品区与阅读角互不干扰,睡眠区遮光与声学细节到位。' },
  { title: '绿色空间 · 会客与茶区', imageA: h5a, imageB: h5b, type: '大平层', area: '约 80㎡', duration: '工期 66 天', desc: '客厅与茶室轴线呼应,木饰面与石材比例克制,适合多代同堂与家庭聚会场景。' },
  { title: '现代混搭 · 老房翻新', imageA: h6a, imageB: h6b, type: '旧房全改', area: '约 100㎡', duration: '工期 76 天', desc: '在原有结构上优化厨卫与管线,复古花砖与定制柜体混搭,控制预算的同时提升居住舒适度。' },
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
    es.forEach(e => { if (e.isIntersecting) { flag.value = true; o.disconnect() } })
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
