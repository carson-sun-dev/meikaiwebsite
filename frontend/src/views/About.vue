<template>
  <div class="inner-page">
    <section class="inner-hero" :style="{ backgroundImage: `url(${heroImg})` }">
      <div class="inner-hero__mask" aria-hidden="true"></div>
      <div class="inner-hero__inner">
        <div class="inner-hero__tag">关 于 美 恺</div>
        <h1 class="inner-hero__title">匠心<span class="accent">{{ deepRootZai }}</span>,筑中原<span class="accent">品质</span></h1>
        <p class="inner-hero__sub">
          始于 {{ foundedYear }} 年,以可落地的方案、可验证的工艺、可追踪的交付,陪伴每一位客户走完装修旅程
        </p>
      </div>
    </section>

    <!-- Metrics:4 项核心数据,跟首页 HomeStatsSection 风格一致 -->
    <section class="about-metrics-wrap">
      <div class="mk-container">
        <div class="about-metrics-grid">
          <div class="about-metric">
            <div class="about-metric__value">{{ metricYearsPlus }}</div>
            <div class="about-metric__label">河 南 本 地 深 耕</div>
          </div>
          <div class="about-metric">
            <div class="about-metric__value">380<span class="about-metric__plus">+</span></div>
            <div class="about-metric__label">累 计 项 目 交 付</div>
          </div>
          <div class="about-metric">
            <div class="about-metric__value">40<span class="about-metric__plus">+</span></div>
            <div class="about-metric__label">服 务 企 业 客 户</div>
          </div>
          <div class="about-metric">
            <div class="about-metric__value">30<span class="about-metric__plus">年</span></div>
            <div class="about-metric__label">总 工 实 战 经 验</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Intro:两块介绍卡 -->
    <section class="mk-section inner-section">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi1" :class="{ 'is-visible': v1 }">
          <span class="mk-eyebrow">Our Story</span>
          <h2 class="mk-title">深耕中原,匠心筑造</h2>
        </header>
        <div class="about-intro-grid">
          <article
            v-for="(item, i) in introBlocks"
            :key="item.title"
            class="about-intro-card"
            :class="{ 'is-visible': v1 }"
            :style="{ transitionDelay: `${i * 0.1}s` }"
          >
            <h3 class="about-intro-card__title">{{ item.title }}</h3>
            <ul class="about-intro-card__list">
              <li v-for="(line, j) in item.bullets" :key="j">{{ line }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
      <span class="mk-divider__seal"></span>
    </div>

    <!-- Timeline:三段历程 -->
    <section class="mk-section inner-section inner-section--alt">
      <div class="mk-container">
        <header class="mk-section-header" ref="hi2" :class="{ 'is-visible': v2 }">
          <span class="mk-eyebrow">Meikai Timeline</span>
          <h2 class="mk-title">从创立到规模化的三次跨越</h2>
        </header>
        <!-- 用户反馈:用之前的时间轴(track + dot + 卡片) v2 颜色 -->
        <div class="about-timeline">
          <article
            v-for="(t, i) in timeline"
            :key="t.period"
            class="timeline-item"
            :class="{ 'is-visible': v2 }"
            :style="{ transitionDelay: `${i * 0.12}s` }"
          >
            <div class="timeline-item__track" aria-hidden="true">
              <span class="timeline-item__dot"></span>
            </div>
            <div class="timeline-item__period">{{ t.period }}</div>
            <div class="timeline-item__card">
              <div class="timeline-item__content">
                <h3 class="timeline-item__title">{{ t.title }}</h3>
                <p class="timeline-item__text">{{ t.text }}</p>
              </div>
              <div class="timeline-item__media">
                <img :src="t.img" alt="" class="timeline-item__img" />
              </div>
            </div>
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
import heroImg from '@/source/about/1.webp'
import m1 from '@/source/about/2/1.webp'
import m2 from '@/source/about/2/2.webp'
import m3 from '@/source/about/2/3.webp'
import { COMPANY_FOUNDED_YEAR, getMetricYearsPlus, getZhYearsZaiPhrase } from '@/utils/companyTimeline'

const metricYearsPlus = getMetricYearsPlus()
const deepRootZai = getZhYearsZaiPhrase()
const foundedYear = COMPANY_FOUNDED_YEAR

const introBlocks = [
  {
    title: '深耕中原,匠心筑造品质标杆',
    bullets: [
      `始于 ${foundedYear} 年,聚焦店铺、商务办公、精品家装三大场景。`,
      '以郑州为核心,服务覆盖洛阳、开封、驻马店等河南多地。',
      '坚持"方案可落地、工艺可验证、交付可追踪"的项目管理标准。',
    ],
  },
  {
    title: '三十年工程积淀,全球直供正品保障',
    bullets: [
      '总工程师团队具备 30 年以上施工与管理经验。',
      '采用一对一深度对接机制,确保关键节点沟通透明。',
      '与立邦、多乐士、三棵树、诺贝尔、公牛、老板等品牌合作,保障正品与环保标准。',
    ],
  },
] as const

const timeline = [
  {
    period: `${foundedYear} - 2020`,
    title: '品牌创立与标准搭建',
    text: '公司创立后快速建立设计、施工、交付协同机制,形成覆盖店铺、商务办公与家庭装饰的标准化服务流程。',
    img: m1,
  },
  {
    period: '2021 - 2024',
    title: '口碑沉淀与区域扩张',
    text: '持续服务河南多地客户,累计企业合作 60+,并与多家标杆餐饮品牌建立长期合作关系,交付质量与效率获得广泛认可。',
    img: m2,
  },
  {
    period: '2025 - 至今',
    title: '规模增长与能力进阶',
    text: '累计实现店铺交付 150+、商务办公 30+、家庭装修 200+,并持续优化工程管理体系,实现项目规模与品质双增长。',
    img: m3,
  },
] as const

const hi1 = ref<HTMLElement | null>(null)
const hi2 = ref<HTMLElement | null>(null)
const v1 = ref(false); const v2 = ref(false)
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
    v1.value = v2.value = true
    return
  }
  observe(hi1.value, v1); observe(hi2.value, v2)
})
onUnmounted(() => { observers.forEach(o => o.disconnect()) })
</script>

<style scoped>
/* Metrics:紧贴 hero 下方,跟首页 HomeStatsSection 一致风格 */
.about-metrics-wrap {
  padding: 56px 24px 64px;
  background: var(--mk-paper);
  border-bottom: 1px solid var(--mk-line);
}
.about-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}
@media (max-width: 900px) {
  .about-metrics-grid { grid-template-columns: repeat(2, 1fr); gap: 28px 16px; }
}
.about-metric {
  text-align: center;
  position: relative;
}
.about-metric:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 14px; bottom: 14px;
  right: -16px;
  width: 1px;
  background: var(--mk-line);
}
@media (max-width: 900px) {
  .about-metric:not(:last-child)::after { display: none; }
}
.about-metric__value {
  font-family: var(--mk-font-serif);
  font-size: clamp(40px, 5vw, 56px);
  font-weight: 600;
  color: var(--mk-brand);
  line-height: 1;
}
.about-metric__plus {
  font-size: 18px;
  color: var(--mk-gold);
  margin-left: 2px;
}
.about-metric__label {
  font-size: 12px;
  color: var(--mk-ink-3);
  margin-top: 12px;
  letter-spacing: 0.32em;
}

/* Intro 2 卡片块 */
.about-intro-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}
@media (max-width: 900px) { .about-intro-grid { grid-template-columns: 1fr; } }
.about-intro-card {
  background: var(--mk-card);
  border: 1px solid var(--mk-line);
  border-left: 3px solid var(--mk-brand);
  border-radius: 0 6px 6px 0;
  padding: 36px 32px;
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.about-intro-card.is-visible { opacity: 1; transform: translateY(0); }
.about-intro-card__title {
  font-family: var(--mk-font-serif);
  font-size: 20px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 18px;
  letter-spacing: 0.05em;
}
.about-intro-card__list {
  margin: 0; padding-left: 1.2em;
  display: flex; flex-direction: column;
  gap: 10px;
}
.about-intro-card__list li {
  font-size: 14px;
  color: var(--mk-ink-2);
  line-height: 1.85;
  letter-spacing: 0.02em;
}

/* Timeline:垂直时间轴(用户反馈恢复原设计,v2 配色) */
.about-timeline {
  position: relative;
  max-width: 920px;
  margin: 0 auto;
}

.timeline-item {
  display: grid;
  grid-template-columns: 48px 140px 1fr;
  gap: 24px;
  align-items: flex-start;
  padding: 24px 0;
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.timeline-item.is-visible { opacity: 1; transform: translateY(0); }

/* track:垂直暗金线;dot:朱红圆点 */
.timeline-item__track {
  position: relative;
  width: 48px;
  align-self: stretch;
  display: flex;
  justify-content: center;
  padding-top: 8px;
}
.timeline-item__track::before {
  content: '';
  position: absolute;
  top: 0; bottom: -48px;
  left: 50%;
  width: 1px;
  background: linear-gradient(180deg, var(--mk-gold-soft), var(--mk-gold) 40%, var(--mk-gold) 60%, var(--mk-gold-soft));
  transform: translateX(-50%);
}
/* 最后一段不延伸 */
.timeline-item:last-child .timeline-item__track::before { bottom: 50%; }
.timeline-item__dot {
  position: relative;
  z-index: 1;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--mk-card);
  border: 3px solid var(--mk-brand);
  margin-top: 6px;
  box-shadow: 0 0 0 4px rgba(196, 30, 58, 0.08);
}

/* 期间标签 */
.timeline-item__period {
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 16px;
  font-weight: 500;
  color: var(--mk-brand);
  letter-spacing: 0.06em;
  padding-top: 10px;
}

/* 卡片(右侧主内容:左字 + 右图) */
.timeline-item__card {
  background: var(--mk-card);
  border: 1px solid var(--mk-line);
  border-radius: 6px;
  overflow: hidden;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}
.timeline-item__card:hover {
  border-color: rgba(196, 30, 58, 0.4);
  box-shadow: var(--mk-shadow-md);
  transform: translateX(4px);
}
.timeline-item__content {
  padding: 24px 26px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.timeline-item__title {
  font-family: var(--mk-font-serif);
  font-size: 19px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 12px;
  letter-spacing: 0.04em;
}
.timeline-item__text {
  margin: 0;
  font-size: 13.5px;
  color: var(--mk-ink-3);
  line-height: 1.85;
}
.timeline-item__media {
  min-height: 160px;
  overflow: hidden;
}
.timeline-item__img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
}

/* 移动端:track 缩窄 + period 移到卡片内顶部 + 卡片图片下移 */
@media (max-width: 900px) {
  .timeline-item {
    grid-template-columns: 32px 1fr;
    gap: 16px;
    padding: 16px 0;
  }
  .timeline-item__track { width: 32px; }
  .timeline-item__period {
    grid-column: 2;
    grid-row: 1;
    padding-top: 4px;
    font-size: 14px;
  }
  .timeline-item__card {
    grid-column: 2;
    grid-row: 2;
    grid-template-columns: 1fr;
    margin-top: 10px;
  }
  .timeline-item__card:hover { transform: none; }
  .timeline-item__media {
    min-height: 160px;
    order: -1;       /* 移动端图片放卡片顶 */
  }
  .timeline-item__content { padding: 20px 20px 24px; }
}

@media (prefers-reduced-motion: reduce) {
  .about-intro-card, .timeline-item {
    opacity: 1; transform: none !important; transition: none;
  }
  .timeline-item__card:hover { transform: none !important; }
}

/* 触摸屏:timeline 卡边框朱红默认激活,取消 hover translateX 避免点击闪烁 */
@media (hover: none) and (pointer: coarse) {
  .timeline-item__card { border-color: rgba(196, 30, 58, 0.28); }
  .timeline-item__card:hover { transform: none !important; }
}
</style>
