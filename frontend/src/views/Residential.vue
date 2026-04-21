<template>
  <div class="res-page">
    <div class="res-page__navbg" aria-hidden="true">
      <NavigationBar />
    </div>

    <main class="res-page__main">
      <section class="res-hero">
        <div class="res-wrap res-hero__inner">
          <p class="res-hero__kicker">RESIDENTIAL INTERIOR</p>
          <h1 class="res-hero__title">精品家装，打造长期舒适的生活场景</h1>
          <p class="res-hero__desc">
            从户型优化到收纳系统，再到材质与灯光配置，为家庭空间提供兼顾美感、实用和耐久性的整体方案。
          </p>
          <div class="res-hero__actions">
            <router-link class="res-btn res-btn--primary" to="/contact">获取家装报价</router-link>
            <router-link class="res-btn res-btn--ghost" to="/about">了解美恺团队</router-link>
          </div>
        </div>
      </section>

      <section class="res-highlights">
        <div class="res-wrap res-highlights__grid">
          <h2 class="res-section__title">为什么业主选择我们</h2>
          <article v-for="item in highlights" :key="item.title" class="res-highlight-card">
            <h3 class="res-highlight-card__title">{{ item.title }}</h3>
            <p class="res-highlight-card__text">{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section class="res-process">
        <div class="res-wrap">
          <h2 class="res-section__title">家装服务流程</h2>
          <div class="res-process__list">
            <div v-for="(step, idx) in processSteps" :key="step.title" class="res-process-item">
              <span class="res-process-item__index">{{ String(idx + 1).padStart(2, '0') }}</span>
              <h3 class="res-process-item__title">{{ step.title }}</h3>
              <p class="res-process-item__desc">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="res-pricing">
        <div class="res-wrap">
          <h2 class="res-section__title">报价区间参考</h2>
          <div class="res-pricing__grid">
            <article v-for="item in priceBands" :key="item.label" class="res-price-card">
              <p class="res-price-card__label">{{ item.label }}</p>
              <p class="res-price-card__range">{{ item.range }}</p>
              <p class="res-price-card__hint">{{ item.hint }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="res-cases">
        <div class="res-wrap">
          <h2 class="res-section__title">精品家装案例</h2>
          <div class="res-case-grid">
            <article v-for="item in cases" :key="item.title" class="res-case-card">
              <div class="res-case-card__media">
                <img :src="item.imageA" alt="" class="res-case-card__img" />
                <img :src="item.imageB" alt="" class="res-case-card__img" />
              </div>
              <div class="res-case-card__body">
                <h3 class="res-case-card__title">{{ item.title }}</h3>
                <div class="res-case-card__meta">
                  <span>{{ item.type }}</span>
                  <span>{{ item.area }}</span>
                  <span>{{ item.duration }}</span>
                </div>
                <p class="res-case-card__desc">{{ item.desc }}</p>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="res-cta">
        <div class="res-wrap res-cta__inner">
          <h2 class="res-cta__title">准备开始你的家装计划？</h2>
          <p class="res-cta__desc">请告诉我们户型与需求，快速获得初步建议与预算区间。</p>
          <router-link class="res-btn res-btn--cta" to="/contact">立即咨询</router-link>
        </div>
      </section>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'

import h1a from '@/source/house/1_1.webp'
import h1b from '@/source/house/1_2.webp'
import h2a from '@/source/house/2_1.webp'
import h2b from '@/source/house/2_2.webp'
import h3a from '@/source/house/3_1.webp'
import h3b from '@/source/house/3_2.webp'
import h4a from '@/source/house/4_1.webp'
import h4b from '@/source/house/4_2.webp'
import h5a from '@/source/house/5_1.webp'
import h5b from '@/source/house/5_2.webp'
import h6a from '@/source/house/6_1.webp'
import h6b from '@/source/house/6_2.webp'

const highlights = [
  {
    title: '空间实用优先',
    text: '以家庭成员习惯和收纳需求为核心，优先解决居住效率和长期使用体验。',
  },
  {
    title: '风格统一落地',
    text: '从硬装、软装到灯光系统统一设计，避免“效果图好看，入住后不实用”。',
  },
  {
    title: '施工安心透明',
    text: '关键节点可追踪，材料与工艺标准清晰，交付后提供完善售后支持。',
  },
] as const

const processSteps = [
  {
    title: '户型评估与需求沟通',
    desc: '结合家庭结构、生活习惯和预算，明确空间改造重点与风格方向。',
  },
  {
    title: '方案深化与报价确认',
    desc: '完成平面规划、收纳系统和材质搭配，并输出分项报价与施工计划。',
  },
  {
    title: '施工执行与软装收尾',
    desc: '分阶段验收施工质量，落地软装与灯光细节，确保入住体验稳定舒适。',
  },
] as const

const priceBands = [
  {
    label: '舒适基础',
    range: '￥500 / m²',
    hint: '适合刚需改善型家庭，注重实用与基础质感升级。',
  },
  {
    label: '品质进阶',
    range: '￥700 / m²',
    hint: '适合对风格统一和细节工艺有要求的家庭。',
  },
  {
    label: '高端定制',
    range: '￥900+ / m²',
    hint: '适合大宅及定制需求，强调整体体验与长期耐用性。',
  },
] as const

/** 精品家装案例：与 source/house 下 1～6 组图片一一对应 */
const cases = [
  {
    title: '现代轻奢 · 一体化设计',
    imageA: h1a,
    imageB: h1b,
    type: '平层三居',
    area: '约 96㎡',
    duration: '工期 58 天',
    desc: '打通客餐厅与厨房视线，全屋灯光分层营造温馨而不浮夸的轻奢质感。',
  },
  {
    title: '极简原木 · 亲子家庭',
    imageA: h2a,
    imageB: h2b,
    type: '居住改善',
    area: '约 106㎡',
    duration: '工期 71 天',
    desc: '以木色与留白为主调，儿童房与书房动静分区，收纳嵌入墙体，方便孩子成长阶段调整。',
  },
  {
    title: '奶油风 · 清新简单',
    imageA: h3a,
    imageB: h3b,
    type: '两居新房',
    area: '约 96㎡',
    duration: '工期 64 天',
    desc: '圆弧收口与柔和色系统一全屋，小户型通过镜面与灯光拉伸视觉，兼顾收纳与颜值。',
  },
  {
    title: '台式简约 · 主卧套间',
    imageA: h4a,
    imageB: h4b,
    type: '套房改造',
    area: '约 112㎡',
    duration: '工期 72 天',
    desc: '主卧与衣帽、梳妆台合并，床品区与阅读角互不干扰，睡眠区遮光与声学细节到位。',
  },
  {
    title: '绿色空间 · 会客与茶区',
    imageA: h5a,
    imageB: h5b,
    type: '大平层',
    area: '约 80㎡',
    duration: '工期 66 天',
    desc: '客厅与茶室轴线呼应，木饰面与石材比例克制，适合多代同堂与家庭聚会场景。',
  },
  {
    title: '现代混搭 · 老房翻新',
    imageA: h6a,
    imageB: h6b,
    type: '旧房全改',
    area: '约 100㎡',
    duration: '工期 76 天',
    desc: '在原有结构上优化厨卫与管线，复古花砖与定制柜体混搭，控制预算的同时提升居住舒适度。',
  },
] as const
</script>

<style scoped>
.res-page { min-height: 100dvh; background: #f4f4f4; color: #000; }
.res-page__navbg { background: #000; }
.res-page__main { padding: 1rem 0 3.6rem; }
.res-page__main > section {
  opacity: 0;
  transform: translateY(14px);
  animation: section-fade-in 0.6s ease forwards;
}
.res-page__main > section:nth-child(1) { animation-delay: 0.04s; }
.res-page__main > section:nth-child(2) { animation-delay: 0.1s; }
.res-page__main > section:nth-child(3) { animation-delay: 0.16s; }
.res-page__main > section:nth-child(4) { animation-delay: 0.22s; }
.res-page__main > section:nth-child(5) { animation-delay: 0.28s; }
.res-page__main > section:nth-child(6) { animation-delay: 0.34s; }
.res-wrap { width: 100%; max-width: 1160px; margin: 0 auto; padding: 0 1.5rem; box-sizing: border-box; }
.res-hero { padding: 1.4rem 0 1.9rem; }
.res-hero__inner { border-radius: 24px; padding: 2.1rem; background: linear-gradient(145deg, #231f20 0%, #3a2d2a 100%); color: #fff; }
.res-hero__kicker { margin: 0; font-size: .78rem; letter-spacing: .14em; font-weight: 700; color: rgba(255,255,255,.72); }
.res-hero__title { margin: .65rem 0 0; font-size: clamp(1.8rem, 3vw + .8rem, 2.9rem); line-height: 1.15; letter-spacing: -.03em; }
.res-hero__desc { max-width: 48rem; margin: .9rem 0 0; font-size: 1.02rem; line-height: 1.7; color: rgba(255,255,255,.84); }
.res-hero__actions { display: flex; gap: 12px; margin-top: 1.4rem; flex-wrap: wrap; }
.res-btn { display: inline-flex; align-items: center; justify-content: center; height: 42px; padding: 0 18px; border-radius: 999px; text-decoration: none; font-size: 14px; font-weight: 700; transition: transform .18s ease; }
.res-btn:hover { transform: translateY(-1px); }
.res-btn--primary { background: #fff; color: #111; }
.res-btn--ghost { border: 1px solid rgba(255,255,255,.36); color: #fff; }
.res-section__title { margin: 0; font-size: clamp(1.4rem, 2.3vw, 2rem); line-height: 1.2; font-weight: 800; letter-spacing: -.02em; }
.res-highlights { padding: 1.8rem 0 1.2rem; }
.res-highlights__grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }
.res-highlights__grid .res-section__title { grid-column: 1 / -1; }
.res-highlight-card { border-radius: 16px; padding: 22px 16px 23px; border: 1px solid rgba(0,0,0,.08); background: #fff; box-shadow: 0 10px 20px rgba(0,0,0,.04); transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.res-highlight-card:hover { transform: translateY(-5px); box-shadow: 0 18px 36px rgba(0,0,0,.1); border-color: rgba(0,0,0,.12); }
.res-highlight-card__title { margin: 0; font-size: 1.04rem; font-weight: 800; }
.res-highlight-card__text { margin: .55rem 0 0; font-size: .92rem; line-height: 1.65; color: rgba(0,0,0,.74); }
.res-process { padding: 1.9rem 0 1.4rem; }
.res-process__list { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; margin-top: 1rem; }
.res-process-item { padding: 10px 2px 8px; border-top: 2px solid rgba(0,0,0,.16); }
.res-process-item__index { display: inline-block; font-size: .75rem; letter-spacing: .08em; color: rgba(0,0,0,.5); font-weight: 800; }
.res-process-item__title { margin: .5rem 0 0; font-size: 1.03rem; line-height: 1.28; }
.res-process-item__desc { margin: .5rem 0 0; font-size: .9rem; line-height: 1.62; color: rgba(0,0,0,.72); }
.res-pricing { padding: 1.8rem 0 2rem; }
.res-pricing__grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; margin-top: 1rem; }
.res-price-card { border-radius: 16px; padding: 22px 16px 23px; background: linear-gradient(180deg, #fff 0%, #f9f9f9 100%); border: 1px solid rgba(0,0,0,.08); transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.res-price-card:hover { transform: translateY(-5px); box-shadow: 0 18px 36px rgba(0,0,0,.1); border-color: rgba(0,0,0,.12); }
.res-price-card__label { margin: 0; font-size: .85rem; font-weight: 700; color: rgba(0,0,0,.55); }
.res-price-card__range { margin: .35rem 0 0; font-size: 1.15rem; font-weight: 900; letter-spacing: -.02em; }
.res-price-card__hint { margin: .55rem 0 0; font-size: .9rem; line-height: 1.6; color: rgba(0,0,0,.72); }
.res-cases { padding: 2rem 0 1.6rem; }
.res-case-grid { margin-top: 1rem; display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px; }
.res-case-card { border-radius: 18px; overflow: hidden; border: 1px solid rgba(0,0,0,.08); background: #fff; }
.res-case-card__media { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }
.res-case-card__img { width: 100%; height: 180px; object-fit: cover; }
.res-case-card__body { padding: 16px 14px 18px; }
.res-case-card__title { margin: 0; font-size: 1rem; font-weight: 800; line-height: 1.3; }
.res-case-card__meta { margin-top: .4rem; display: flex; flex-wrap: wrap; gap: 8px; font-size: .78rem; color: rgba(0,0,0,.55); }
.res-case-card__desc { margin: .55rem 0 0; font-size: .9rem; line-height: 1.62; color: rgba(0,0,0,.74); }
.res-cta { padding: 2rem 0 .8rem; }
.res-cta__inner { border-radius: 22px; padding: 1.8rem; background: #fff; border: 1px solid rgba(0,0,0,.08); text-align: center; }
.res-cta__title { margin: 0; font-size: clamp(1.3rem, 2vw, 1.8rem); }
.res-cta__desc { margin: .55rem auto 1rem; max-width: 40rem; color: rgba(0,0,0,.68); line-height: 1.65; }
.res-cta .res-btn--cta {
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
.res-cta .res-btn--cta:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}
@media (max-width: 980px) and (min-width: 768px) {
  .res-highlights__grid,
  .res-process__list,
  .res-pricing__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .res-highlights__grid .res-section__title {
    grid-column: 1 / -1;
  }

  .res-case-grid {
    grid-template-columns: 1fr;
  }

  .res-hero {
    padding: 1.8rem 0 2.1rem;
  }

  .res-hero__inner {
    padding: 1rem 1.35rem 1.5rem !important;
  }

  .res-hero__kicker {
    padding-top: 0.3rem;
  }

  .res-hero__title {
    margin-top: 0.9rem;
  }

  .res-hero__actions {
    margin-top: 1.7rem;
  }

  .res-wrap {
    padding: 0 1.25rem;
  }
}

@media (max-width: 767px) {
  .res-highlights__grid,
  .res-process__list,
  .res-pricing__grid,
  .res-case-grid {
    grid-template-columns: 1fr;
  }

  .res-hero {
    padding: 1.9rem 0 2.2rem;
  }

  .res-hero__inner {
    padding: 0.5rem 1.1rem 1rem !important;
  }

  .res-hero__kicker {
    padding-top: 0.35rem;
  }

  .res-hero__title {
    margin-top: 0.85rem;
  }

  .res-hero__actions {
    margin-top: 1.75rem;
  }

  .res-wrap {
    padding: 0 1rem;
  }

  .res-case-card__img {
    height: 168px;
  }

  .res-cta__inner {
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
  .res-page__main > section {
    opacity: 1;
    transform: none;
    animation: none;
  }
  .res-highlight-card,
  .res-price-card { transition: none; }
  .res-highlight-card:hover,
  .res-price-card:hover { transform: none; }
}
</style>
