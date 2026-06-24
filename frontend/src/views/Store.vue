<template>
  <div class="inner-page">
    <!-- NavigationBar 全局 fixed 在 App.vue -->

    <section class="inner-hero" :style="{ backgroundImage: `url(${heroImg})` }">
      <div class="inner-hero__mask" aria-hidden="true"></div>
      <div class="inner-hero__inner">
        <div class="inner-hero__tag">品 牌 · 店 装</div>
        <h1 class="inner-hero__title">不止<span class="accent">好看</span>,更要<span class="accent">高效开业</span></h1>
        <p class="inner-hero__sub">
          为餐饮、零售与服务业门店提供从品牌识别到开业交付的完整方案,把停业时间和预算风险降到最低
        </p>
      </div>
    </section>

    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi1" :class="{ 'is-visible': v1 }">
          <span class="mk-eyebrow">Why Stores</span>
          <h2 class="mk-title">为什么很多门店选择我们</h2>
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
          <h2 class="mk-title">店装服务流程</h2>
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
          <h2 class="mk-title">品牌店装案例</h2>
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
                <span>{{ item.industry }}</span>
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
import heroImg from '@/source/store/1_2.webp'

import wuyue1 from '@/source/store/1_1.webp'
import wuyue2 from '@/source/store/1_2.webp'
import fzyShangying1 from '@/source/store/福状元 商英街1.webp'
import fzyShangying2 from '@/source/store/福状元 商英街2.webp'
import shanyouyue1 from '@/source/store/山有月茶餐厅1.webp'
import shanyouyue2 from '@/source/store/山有月茶餐厅2.webp'
import fzyLuoyang1 from '@/source/store/福状元 洛阳分店1.webp'
import fzyLuoyang2 from '@/source/store/福状元洛阳分店2.webp'
import yangzhanggui1 from '@/source/store/杨掌柜辣椒炒肉 太康二路店.webp'
import yangzhanggui2 from '@/source/store/杨掌柜辣椒炒肉 太康二路店2.webp'
import fzyPingdingshan1 from '@/source/store/福状元平顶山分店.webp'
import fzyPingdingshan2 from '@/source/store/福状元平顶山分店2.webp'
import caida1 from '@/source/store/河南财经政法大学食堂1.webp'
import caida2 from '@/source/store/河南财经大学食堂2.webp'
import fzyYingxie1 from '@/source/store/福状元英协路1.webp'
import fzyYingxie2 from '@/source/store/福状元英协路2.webp'
import tea1 from '@/source/store/茶舍1.webp'
import tea2 from '@/source/store/茶舍2.webp'
import fzySuoling1 from '@/source/store/福状元索凌路1.webp'
import fzySuoling2 from '@/source/store/福状元索凌路2.webp'

const highlights = [
  { title: '快节奏开店', text: '以节点倒排施工计划,减少无效等待,尽量缩短开业准备周期。' },
  { title: '品牌识别落地', text: '统一门头、前台、灯光等材质,让空间与品牌调性一致。' },
  { title: '预算透明可控', text: '从主材到施工项分级拆分,前期明确关键变量,避免后期失控。' },
] as const

const processSteps = [
  { title: '需求诊断与量房', desc: '明确业态、客群与经营目标,现场测量并梳理强弱电、排烟、消防等约束条件。' },
  { title: '方案设计与预算拆解', desc: '以客户需求为主、设计效果与施工图,同时给出分项报价与材料建议。' },
  { title: '施工交付与验收', desc: '按节点推进施工,定期复盘进度与质量,完工后进行全项验收与交付培训。' },
] as const

const priceBands = [
  { label: '标准升级', range: '¥800 - ¥1000 / m²', hint: '适合轻餐、零售标准化门店,重点优化灯光和基础形象。' },
  { label: '品牌强化', range: '¥1000 - ¥1500 / m²', hint: '适合有品牌调性要求的主力门店,兼顾视觉和功能效率。' },
  { label: '旗舰定制', range: '¥1500+ / m²', hint: '适合旗舰或体验型空间,强调差异化体验与材料细节。' },
] as const

const cases = [
  { title: '福状元 · 吾悦广场店', imageA: wuyue1, imageB: wuyue2, industry: '餐饮', area: '约 210㎡', duration: '工期 43 天', desc: '围绕翻台效率重做前后场区分,重点优化门头识别、等位区体验与后厨衔接。' },
  { title: '福状元 · 商英街店', imageA: fzyShangying1, imageB: fzyShangying2, industry: '餐饮', area: '约 180㎡', duration: '工期 35 天', desc: '郑州商英街粥品门店形象升级,服务区与就餐区清晰,兼顾高峰出餐与就餐舒适度。' },
  { title: '山有月茶餐厅', imageA: shanyouyue1, imageB: shanyouyue2, industry: '茶饮简餐', area: '约 220㎡', duration: '工期 45 天', desc: '茶餐厅氛围与灯光层次落地,卡座与过道尺度兼顾私密与翻台,呈现温馨待客场景。' },
  { title: '福状元 · 洛阳分店', imageA: fzyLuoyang1, imageB: fzyLuoyang2, industry: '餐饮', area: '约 240㎡', duration: '工期 46 天', desc: '洛阳分店空间与总部形象统一,门头识别与室内主材选型可控,保障异地复制效率。' },
  { title: '杨掌柜辣椒炒肉 · 太康二路店', imageA: yangzhanggui1, imageB: yangzhanggui2, industry: '中式正餐', area: '约 150㎡', duration: '工期 40 天', desc: '太康二路热炒门店重油烟与明厨展示并重,排风与灯光配合菜品呈现,提升就餐区舒适度。' },
  { title: '福状元 · 平顶山分店', imageA: fzyPingdingshan1, imageB: fzyPingdingshan2, industry: '餐饮', area: '约 230㎡', duration: '工期 44 天', desc: '平顶山门店从门头到就餐区一体化交付,材质与工艺与品牌手册对齐,便于后期运维。' },
  { title: '河南财经政法大学 · 食堂改造', imageA: caida1, imageB: caida2, industry: '大众食堂', area: '约 900㎡', duration: '工期 72 天', desc: '高校食堂档口与就餐大厅分区明确,人流线与取餐动线优化,满足集中就餐高峰。' },
  { title: '福状元 · 英协路店', imageA: fzyYingxie1, imageB: fzyYingxie2, industry: '餐饮', area: '约 210㎡', duration: '工期 40 天', desc: '郑州英协路临街店招与室内统一设计语言,前场展示与后场备餐分区合理,保障出餐效率。' },
  { title: '精品茶舍空间', imageA: tea1, imageB: tea2, industry: '茶空间', area: '约 170㎡', duration: '工期 35 天', desc: '茶舍静谧氛围与展陈结合,照明与材质突出茶品陈列,兼顾品茗与社交场景。' },
  { title: '福状元 · 索凌路店', imageA: fzySuoling1, imageB: fzySuoling2, industry: '餐饮', area: '约 225㎡', duration: '工期 43 天', desc: '郑州索凌路门店从门头到室内完整落地,桌椅与灯光匹配品牌调性,交付即可开业。' },
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

<!-- 样式与 Business.vue 同源:把 .inner-page 系列样式提到 home-page.css 公共类(下轮),
     目前简洁起见 import Business 的 css 还做不到 scoped,直接复用 Business 内联同样的样式块。
     为避免重复,这里只保留 page 容器,具体 inner-* 样式由全局 home-page.css 提供(已下轮抽出)。 -->
<style scoped>
.inner-page { min-height: 100dvh; background: var(--mk-paper); color: var(--mk-ink); font-family: var(--mk-font-sans); }
</style>
