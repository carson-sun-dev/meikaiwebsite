<template>
  <div class="business-page">
    <div class="business-page__navbg" aria-hidden="true">
      <NavigationBar />
    </div>

    <main class="business-page__main">
      <section class="business-hero">
        <div class="business-wrap business-hero__inner">
          <p class="business-hero__kicker">OFFICE INTERIOR SOLUTION</p>
          <h1 class="business-hero__title">商务办公空间，兼顾效率与品牌感</h1>
          <p class="business-hero__desc">
            聚焦企业办公场景，围绕协作效率、员工体验与企业形象，提供从规划设计到工程交付的一体化服务。
          </p>
          <div class="business-hero__actions">
            <router-link class="business-btn business-btn--primary" to="/contact">获取办公报价</router-link>
            <router-link class="business-btn business-btn--ghost" to="/about">了解美恺团队</router-link>
          </div>
        </div>
      </section>

      <section class="business-highlights">
        <div class="business-wrap business-highlights__grid">
          <h2 class="business-section__title">为什么企业客户选择我们</h2>
          <article v-for="item in highlights" :key="item.title" class="business-highlight-card">
            <h3 class="business-highlight-card__title">{{ item.title }}</h3>
            <p class="business-highlight-card__text">{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section class="business-process">
        <div class="business-wrap">
          <h2 class="business-section__title">办公项目服务流程</h2>
          <div class="business-process__list">
            <div v-for="(step, idx) in processSteps" :key="step.title" class="business-process-item">
              <span class="business-process-item__index">{{ String(idx + 1).padStart(2, '0') }}</span>
              <h3 class="business-process-item__title">{{ step.title }}</h3>
              <p class="business-process-item__desc">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="business-pricing">
        <div class="business-wrap">
          <h2 class="business-section__title">报价区间参考</h2>
          <div class="business-pricing__grid">
            <article v-for="item in priceBands" :key="item.label" class="business-price-card">
              <p class="business-price-card__label">{{ item.label }}</p>
              <p class="business-price-card__range">{{ item.range }}</p>
              <p class="business-price-card__hint">{{ item.hint }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="business-cases">
        <div class="business-wrap">
          <h2 class="business-section__title">商务办公案例</h2>
          <div class="business-case-grid">
            <article v-for="item in cases" :key="item.title" class="business-case-card">
              <div class="business-case-card__media">
                <img :src="item.imageA" alt="" class="business-case-card__img" />
                <img :src="item.imageB" alt="" class="business-case-card__img" />
              </div>
              <div class="business-case-card__body">
                <h3 class="business-case-card__title">{{ item.title }}</h3>
                <div class="business-case-card__meta">
                  <span>{{ item.type }}</span>
                  <span>{{ item.area }}</span>
                  <span>{{ item.duration }}</span>
                </div>
                <p class="business-case-card__desc">{{ item.desc }}</p>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="business-cta">
        <div class="business-wrap business-cta__inner">
          <h2 class="business-cta__title">想升级你的办公空间？</h2>
          <p class="business-cta__desc">请告诉我们面积与需求，我们将提供初步平面建议和预算区间。</p>
          <router-link class="business-btn business-btn--cta" to="/contact">立即咨询</router-link>
        </div>
      </section>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'

import bus1a from '@/source/business/b1_1.webp'
import bus1b from '@/source/business/b1_2.webp'
import bus2a from '@/source/business/b2_1.webp'
import bus2b from '@/source/business/b2_2.webp'
import bus3a from '@/source/business/b3_1.webp'
import bus3b from '@/source/business/b3_2.webp'
import bus4a from '@/source/business/b4_1.webp'
import bus4b from '@/source/business/b4_2.webp'

const highlights = [
  {
    title: '效率导向布局',
    text: '围绕部门协作和会议频次规划空间，减少无效跑动，提升团队沟通效率。',
  },
  {
    title: '企业形象统一',
    text: '前台、会客区、开放办公与文化墙风格统一，强化品牌识别与客户第一印象。',
  },
  {
    title: '工期与成本可控',
    text: '节点化管理施工流程，预算按分项透明拆解，降低追加和延期风险。',
  },
] as const

const processSteps = [
  {
    title: '需求调研与办公诊断',
    desc: '了解团队规模、岗位协同和未来扩编计划，明确功能分区与空间优先级。',
  },
  {
    title: '平面优化与预算确认',
    desc: '深度优化办公区域与工位排布，明码标价、绝无隐形消费的预算方案。',
  },
  {
    title: '施工管理与交付培训',
    desc: '按节点推进施工及验收，完成交付后提供空间使用与维护建议。',
  },
] as const

const priceBands = [
  {
    label: '标准办公',
    range: '￥400 - ￥700 / m²',
    hint: '适合中小企业基础升级，优先保证工位效率与会议功能。',
  },
  {
    label: '形象升级',
    range: '￥700 - ￥1000 / m²',
    hint: '适合注重品牌展示和员工体验的成长型团队。',
  },
  {
    label: '总部定制',
    range: '￥1000+ / m²',
    hint: '适合总部或综合办公空间，强调品牌表达和高品质细节。',
  },
] as const

/** 商务办公案例：与 source/business 下 b1～b4 成对图片一一对应 */
const cases = [
  {
    title: '科技服务企业 · 开放办公与协作区',
    imageA: bus1a,
    imageB: bus1b,
    type: '开放办公',
    area: '约 380㎡',
    duration: '工期 52 天',
    desc: '工位区与协作区一体化布局，照明与声学处理兼顾专注与讨论，动线缩短跨部门沟通成本。',
  },
  {
    title: '品牌咨询公司 · 接待与会议空间',
    imageA: bus2a,
    imageB: bus2b,
    type: '形象办公',
    area: '约 290㎡',
    duration: '工期 53 天',
    desc: '前台形象墙与访客串联会议室，材质与灯光统一品牌色，提升客户到访第一印象。',
  },
  {
    title: '区域总部 · 高管办公与茶歇区',
    imageA: bus3a,
    imageB: bus3b,
    type: '总部办公',
    area: '约 510㎡',
    duration: '工期 63 天',
    desc: '独立办公室与共享茶歇区相邻布置，既保证决策私密性，又便于管理层与团队快速对齐。',
  },
  {
    title: '成长型团队 · 联合办公改造',
    imageA: bus4a,
    imageB: bus4b,
    type: '办公升级',
    area: '约 220㎡',
    duration: '工期 44 天',
    desc: '在有限面积内重构储物与工位比例，增设电话间与站立会议角，满足扩编前弹性使用。',
  },
] as const
</script>

<style scoped>
.business-page { min-height: 100dvh; background: #f4f4f4; color: #000; }
.business-page__navbg { background: #000; }
.business-page__main { padding: 1.6rem 0 3.6rem; }
.business-page__main > section {
  opacity: 0;
  transform: translateY(14px);
  animation: section-fade-in 0.6s ease forwards;
}
.business-page__main > section:nth-child(1) { animation-delay: 0.04s; }
.business-page__main > section:nth-child(2) { animation-delay: 0.1s; }
.business-page__main > section:nth-child(3) { animation-delay: 0.16s; }
.business-page__main > section:nth-child(4) { animation-delay: 0.22s; }
.business-page__main > section:nth-child(5) { animation-delay: 0.28s; }
.business-page__main > section:nth-child(6) { animation-delay: 0.34s; }
.business-wrap { width: 100%; max-width: 1160px; margin: 0 auto; padding: 0 1.5rem; box-sizing: border-box; }
.business-hero { padding: 2.2rem 0 1.9rem; }
.business-hero__inner { border-radius: 24px; padding: 2.1rem; background: linear-gradient(145deg, #111 0%, #1f2a33 100%); color: #fff; }
.business-hero__kicker { margin: 0; font-size: .78rem; letter-spacing: .14em; font-weight: 700; color: rgba(255,255,255,.72); }
.business-hero__title { margin: .65rem 0 0; font-size: clamp(1.8rem, 3vw + .8rem, 2.9rem); line-height: 1.15; letter-spacing: -.03em; }
.business-hero__desc { max-width: 48rem; margin: .9rem 0 0; font-size: 1.02rem; line-height: 1.7; color: rgba(255,255,255,.84); }
.business-hero__actions { display: flex; gap: 12px; margin-top: 1.4rem; flex-wrap: wrap; }
.business-btn { display: inline-flex; align-items: center; justify-content: center; height: 42px; padding: 0 18px; border-radius: 999px; text-decoration: none; font-size: 14px; font-weight: 700; transition: transform .18s ease; }
.business-btn:hover { transform: translateY(-1px); }
.business-btn--primary { background: #fff; color: #111; }
.business-btn--ghost { border: 1px solid rgba(255,255,255,.36); color: #fff; }
.business-section__title { margin: 0; font-size: clamp(1.4rem, 2.3vw, 2rem); line-height: 1.2; font-weight: 800; letter-spacing: -.02em; }
.business-highlights { padding: 1.8rem 0 1.2rem; }
.business-highlights__grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }
.business-highlights__grid .business-section__title { grid-column: 1 / -1; }
.business-highlight-card { border-radius: 16px; padding: 22px 16px 23px; border: 1px solid rgba(0,0,0,.08); background: #fff; box-shadow: 0 10px 20px rgba(0,0,0,.04); transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.business-highlight-card:hover { transform: translateY(-5px); box-shadow: 0 18px 36px rgba(0,0,0,.1); border-color: rgba(0,0,0,.12); }
.business-highlight-card__title { margin: 0; font-size: 1.04rem; font-weight: 800; }
.business-highlight-card__text { margin: .55rem 0 0; font-size: .92rem; line-height: 1.65; color: rgba(0,0,0,.74); }
.business-process { padding: 1.9rem 0 1.4rem; }
.business-process__list { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; margin-top: 1rem; }
.business-process-item { padding: 10px 2px 8px; border-top: 2px solid rgba(0,0,0,.16); }
.business-process-item__index { display: inline-block; font-size: .75rem; letter-spacing: .08em; color: rgba(0,0,0,.5); font-weight: 800; }
.business-process-item__title { margin: .5rem 0 0; font-size: 1.03rem; line-height: 1.28; }
.business-process-item__desc { margin: .5rem 0 0; font-size: .9rem; line-height: 1.62; color: rgba(0,0,0,.72); }
.business-pricing { padding: 1.8rem 0 2rem; }
.business-pricing__grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; margin-top: 1rem; }
.business-price-card { border-radius: 16px; padding: 22px 16px 23px; background: linear-gradient(180deg, #fff 0%, #f9f9f9 100%); border: 1px solid rgba(0,0,0,.08); transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.business-price-card:hover { transform: translateY(-5px); box-shadow: 0 18px 36px rgba(0,0,0,.1); border-color: rgba(0,0,0,.12); }
.business-price-card__label { margin: 0; font-size: .85rem; font-weight: 700; color: rgba(0,0,0,.55); }
.business-price-card__range { margin: .35rem 0 0; font-size: 1.15rem; font-weight: 900; letter-spacing: -.02em; }
.business-price-card__hint { margin: .55rem 0 0; font-size: .9rem; line-height: 1.6; color: rgba(0,0,0,.72); }
.business-cases { padding: 2rem 0 1.6rem; }
.business-case-grid { margin-top: 1rem; display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px; }
.business-case-card { border-radius: 18px; overflow: hidden; border: 1px solid rgba(0,0,0,.08); background: #fff; }
.business-case-card__media { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }
.business-case-card__img { width: 100%; height: 180px; object-fit: cover; }
.business-case-card__body { padding: 16px 14px 18px; }
.business-case-card__title { margin: 0; font-size: 1rem; font-weight: 800; line-height: 1.3; }
.business-case-card__meta { margin-top: .4rem; display: flex; flex-wrap: wrap; gap: 8px; font-size: .78rem; color: rgba(0,0,0,.55); }
.business-case-card__desc { margin: .55rem 0 0; font-size: .9rem; line-height: 1.62; color: rgba(0,0,0,.74); }
.business-cta { padding: 2rem 0 .8rem; }
.business-cta__inner { border-radius: 22px; padding: 1.8rem; background: #fff; border: 1px solid rgba(0,0,0,.08); text-align: center; }
.business-cta__title { margin: 0; font-size: clamp(1.3rem, 2vw, 1.8rem); }
.business-cta__desc { margin: .55rem auto 1rem; max-width: 40rem; color: rgba(0,0,0,.68); line-height: 1.65; }
.business-cta .business-btn--cta {
  margin-top: 1rem;
  min-width: 120px;
  height: 36px;
  padding: 0 20px;
  border: none;
  background: #ff5449;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}
.business-cta .business-btn--cta:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}
@media (max-width: 980px) and (min-width: 768px) {
  .business-highlights__grid,
  .business-process__list,
  .business-pricing__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .business-highlights__grid .business-section__title {
    grid-column: 1 / -1;
  }

  .business-case-grid {
    grid-template-columns: 1fr;
  }

  .business-hero {
    padding: 2.55rem 0 2.1rem;
  }

  .business-hero__inner {
    padding: 1.85rem 1.35rem 2rem;
  }

  .business-hero__kicker {
    padding-top: 0.3rem;
  }

  .business-hero__title {
    margin-top: 0.9rem;
  }

  .business-hero__actions {
    margin-top: 1.7rem;
  }

  .business-wrap {
    padding: 0 1.25rem;
  }
}

@media (max-width: 767px) {
  .business-highlights__grid,
  .business-process__list,
  .business-pricing__grid,
  .business-case-grid {
    grid-template-columns: 1fr;
  }

  .business-hero {
    padding: 2.65rem 0 2.2rem;
  }

  .business-hero__inner {
    padding: 1.7rem 1.1rem 1.95rem;
  }

  .business-hero__kicker {
    padding-top: 0.35rem;
  }

  .business-hero__title {
    margin-top: 0.85rem;
  }

  .business-hero__actions {
    margin-top: 1.75rem;
  }

  .business-wrap {
    padding: 0 1rem;
  }

  .business-case-card__img {
    height: 168px;
  }

  .business-cta__inner {
    padding: 1.4rem;
  }
}

@keyframes section-fade-in {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .business-page__main > section {
    opacity: 1;
    transform: none;
    animation: none;
  }
  .business-highlight-card,
  .business-price-card { transition: none; }
  .business-highlight-card:hover,
  .business-price-card:hover { transform: none; }
}
</style>
