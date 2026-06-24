<template>
  <section class="mk-section biz-section">
    <div class="mk-container">
      <header class="mk-section-header" ref="headerRef" :class="{ 'is-visible': revealedHeader }">
        <span class="mk-eyebrow">Business Lines</span>
        <h2 class="mk-title">三大业务线</h2>
        <p class="mk-title-sub">店铺 · 办公 · 家装  ·  一站交付</p>
      </header>

      <div class="biz-grid">
        <router-link
          v-for="(b, i) in businessLines"
          :key="b.route"
          :to="b.route"
          class="biz-card"
          :class="{ 'is-visible': revealedCards }"
          :style="{ transitionDelay: `${i * 0.08}s`, '--card-img': `url(${b.img})` }"
        >
          <div class="biz-card__img" aria-hidden="true"></div>
          <div class="biz-card__body">
            <span class="biz-card__tag">{{ b.tag }}</span>
            <h3 class="biz-card__title">{{ b.title }}</h3>
            <div class="biz-card__metric">
              <span class="biz-card__metric-num">{{ b.metricNum }}</span>
              <span class="biz-card__metric-suffix">{{ b.metricSuffix }}</span>
              <span class="biz-card__metric-label">{{ b.metricLabel }}</span>
            </div>
            <p class="biz-card__desc">{{ b.desc }}</p>
            <span class="biz-card__link">点击了解</span>
          </div>
        </router-link>
      </div>
    </div>
  </section>

  <!-- 节区尾部 logo 分隔器 -->
  <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
    <span class="mk-divider__seal"></span>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import logoImg from '@/source/logo/logo.webp'

// 业务顺序按用户指令:店装 → 办公 → 家装
import imgStore from '@/source/store/福状元 商英街1.webp'
import imgBusiness from '@/source/business/b1_1.webp'
import imgHouse from '@/source/house/2_1.webp'

const businessLines = [
  {
    route: '/store',
    img: imgStore,
    tag: 'Storefront',
    title: '品牌店装',
    metricNum: '120',
    metricSuffix: '+',
    metricLabel: '店铺项目',
    desc: '从网红餐饮、品牌零售到高端会所,我们将每一平米都转化为商业价值,助力店主实现从"开业"到"爆火"的跨越。',
  },
  {
    route: '/business',
    img: imgBusiness,
    tag: 'Office',
    title: '商务·办公',
    metricNum: '30',
    metricSuffix: '+',
    metricLabel: '商务项目',
    desc: '为企业提供商务·办公解决方案,构筑激发灵感的创意引擎,让办公空间成为彰显企业实力与格局的窗口。',
  },
  {
    route: '/residential',
    img: imgHouse,
    tag: 'Residential',
    title: '精品家装',
    metricNum: '200',
    metricSuffix: '+',
    metricLabel: '家庭定制',
    desc: '美恺从精品家装起家,对家装保持最深沉的敬畏。从零散图纸到温暖实景,我们始终把客户需求置于首位。',
  },
] as const

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
.biz-section { background: var(--mk-paper); }

.mk-section-header {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.biz-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
@media (max-width: 768px) { .biz-grid { grid-template-columns: 1fr; } }

.biz-card {
  display: flex;
  flex-direction: column;
  background: var(--mk-card);
  overflow: hidden;
  border: 1px solid var(--mk-line);
  border-radius: 6px;
  text-decoration: none;
  color: inherit;
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1),
              box-shadow 0.4s ease, border-color 0.3s ease;
}
.biz-card.is-visible { opacity: 1; transform: translateY(0); }
.biz-card:hover {
  transform: translateY(-8px) !important;
  box-shadow: var(--mk-shadow-md);
  border-color: rgba(196, 30, 58, 0.45);
}

.biz-card__img {
  height: 240px;
  background-image: var(--card-img);
  background-size: cover;
  background-position: center;
  transition: transform 0.6s ease;
}
.biz-card:hover .biz-card__img { transform: scale(1.04); }

.biz-card__body {
  position: relative;
  padding: 36px 28px 32px;
}

.biz-card__tag {
  position: absolute;
  top: -18px;
  left: 28px;
  background: var(--mk-ink);
  color: white;
  padding: 7px 14px;
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 12px;
  letter-spacing: 0.2em;
  border-radius: 2px;
  transition: background-color 0.3s ease;
}
.biz-card:hover .biz-card__tag { background: var(--mk-brand); }

.biz-card__title {
  font-family: var(--mk-font-serif);
  font-size: 26px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 14px;
  letter-spacing: 0.05em;
}

.biz-card__metric {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 18px;
}
.biz-card__metric-num {
  font-family: var(--mk-font-serif);
  font-size: 36px;
  font-weight: 600;
  color: var(--mk-brand);
  line-height: 1;
}
.biz-card__metric-suffix {
  font-family: var(--mk-font-serif);
  font-size: 22px;
  color: var(--mk-gold);
}
.biz-card__metric-label {
  font-size: 12px;
  color: var(--mk-ink-3);
  letter-spacing: 0.3em;
  margin-left: 8px;
}

.biz-card__desc {
  margin: 0 0 22px;
  font-size: 14px;
  color: var(--mk-ink-3);
  line-height: 1.85;
}

.biz-card__link {
  font-size: 12px;
  font-weight: bold;
  color: var(--mk-gold);
  letter-spacing: 0.3em;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: gap 0.3s ease, color 0.3s ease;
}
.biz-card__link::after {
  /* content: '→'; */
  transition: transform 0.3s ease;
}
.biz-card:hover .biz-card__link {
  color: var(--mk-brand);
  gap: 14px;
}
.biz-card:hover .biz-card__link::after { transform: translateX(4px); }

@media (prefers-reduced-motion: reduce) {
  .biz-card { opacity: 1; transform: none !important; transition: none; }
  .biz-card:hover { transform: none !important; }
  .biz-card:hover .biz-card__img { transform: none; }
}

/* 触摸屏:tag 朱红 + 链接朱红 + 箭头位移 默认激活,不再依赖 hover */
@media (hover: none) and (pointer: coarse) {
  .biz-card { border-color: rgba(196, 30, 58, 0.28); }
  .biz-card__tag { background: var(--mk-brand); }
  .biz-card__link { color: var(--mk-brand); gap: 14px; }
  .biz-card__link::after { transform: translateX(4px); }
  .biz-card:hover { transform: none !important; }
  .biz-card:hover .biz-card__img { transform: none; }
}
</style>
