<template>
  <div class="store-page">
    <div class="store-page__navbg" aria-hidden="true">
      <NavigationBar />
    </div>

    <main class="store-page__main">
      <section class="store-hero">
        <div class="store-wrap store-hero__inner">
          <p class="store-hero__kicker">BRAND STORE INTERIOR</p>
          <h1 class="store-hero__title">品牌店装，不止好看，更要高效开业</h1>
          <p class="store-hero__desc">
            围绕客户体验、店铺氛围、品牌感和施工周期，为餐饮、零售、美业等门店提供从设计到交付的一体化落地方案。
          </p>
          <div class="store-hero__actions">
            <router-link class="store-btn store-btn--primary" to="/contact">获取门店报价</router-link>
            <router-link class="store-btn store-btn--ghost" to="/about">了解美恺团队</router-link>
          </div>
        </div>
      </section>

      <section class="store-highlights">
        <div class="store-wrap store-highlights__grid">
          <h2 class="store-section__title">为什么很多门店选择我们</h2>
          <article v-for="item in highlights" :key="item.title" class="store-highlight-card">
            <h3 class="store-highlight-card__title">{{ item.title }}</h3>
            <p class="store-highlight-card__text">{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section class="store-process">
        <div class="store-wrap">
          <h2 class="store-section__title">店装服务流程</h2>
          <div class="store-process__list">
            <div v-for="(step, idx) in processSteps" :key="step.title" class="store-process-item">
              <span class="store-process-item__index">{{ String(idx + 1).padStart(2, '0') }}</span>
              <h3 class="store-process-item__title">{{ step.title }}</h3>
              <p class="store-process-item__desc">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="store-pricing">
        <div class="store-wrap">
          <h2 class="store-section__title">报价区间参考</h2>
          <div class="store-pricing__grid">
            <article v-for="item in priceBands" :key="item.label" class="store-price-card">
              <p class="store-price-card__label">{{ item.label }}</p>
              <p class="store-price-card__range">{{ item.range }}</p>
              <p class="store-price-card__hint">{{ item.hint }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="store-cases">
        <div class="store-wrap">
          <h2 class="store-section__title">品牌店装案例</h2>
          <div class="store-case-grid">
            <article v-for="item in cases" :key="item.title" class="store-case-card">
              <div class="store-case-card__media">
                <img :src="item.imageA" alt="" class="store-case-card__img" />
                <img :src="item.imageB" alt="" class="store-case-card__img" />
              </div>
              <div class="store-case-card__body">
                <h3 class="store-case-card__title">{{ item.title }}</h3>
                <div class="store-case-card__meta">
                  <span>{{ item.industry }}</span>
                  <span>{{ item.area }}</span>
                  <span>{{ item.duration }}</span>
                </div>
                <p class="store-case-card__desc">{{ item.desc }}</p>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="store-cta">
        <div class="store-wrap store-cta__inner">
          <h2 class="store-cta__title">准备启动你的店铺装修项目？</h2>
          <p class="store-cta__desc">请告诉我们工程的基础信息，我们将尽快根据信息反馈初步建议与预算范围。</p>
          <router-link class="store-btn store-btn--cta" to="/contact">立即咨询</router-link>
        </div>
      </section>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'

/* 案例图：文件名即门店/项目配对 */
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
  {
    title: '快节奏开店',
    text: '以节点倒排施工计划，减少无效等待，尽量缩短开业准备周期。',
  },
  {
    title: '品牌识别落地',
    text: '统一门头、前台、灯光等材质，让空间与品牌调性一致。',
  },
  {
    title: '预算透明可控',
    text: '从主材到施工项分级拆分，前期明确关键变量，避免后期失控。',
  },
] as const

const processSteps = [
  {
    title: '需求诊断与量房',
    desc: '明确业态、客群与经营目标，现场测量并梳理强弱电、排烟、消防等约束条件。',
  },
  {
    title: '方案设计与预算拆解',
    desc: '以客户需求为主、设计效果与施工图，同时给出分项报价与材料建议。',
  },
  {
    title: '施工交付与验收',
    desc: '按节点推进施工，定期复盘进度与质量，完工后进行全项验收与交付培训。',
  },
] as const

const priceBands = [
  {
    label: '标准升级',
    range: '￥800 - ￥1000 / m²',
    hint: '适合轻餐、零售标准化门店，重点优化灯光和基础形象。',
  },
  {
    label: '品牌强化',
    range: '￥1000 - ￥1500 / m²',
    hint: '适合有品牌调性要求的主力门店，兼顾视觉和功能效率。',
  },
  {
    label: '旗舰定制',
    range: '￥1500+ / m²',
    hint: '适合旗舰或体验型空间，强调差异化体验与材料细节。',
  },
] as const

/** 品牌店装案例：福状元与其他品牌穿插展示，图片与文件名一一对应 */
const cases = [
  {
    title: '福状元 · 吾悦广场店',
    imageA: wuyue1,
    imageB: wuyue2,
    industry: '餐饮',
    area: '约 210㎡',
    duration: '工期 43 天',
    desc: '围绕翻台效率重做前后场区分，重点优化门头识别、等位区体验与后厨衔接。',
  },
  {
    title: '福状元 · 商英街店',
    imageA: fzyShangying1,
    imageB: fzyShangying2,
    industry: '餐饮',
    area: '约 180㎡',
    duration: '工期 35 天',
    desc: '郑州商英街粥品门店形象升级，服务区与就餐区清晰，兼顾高峰出餐与就餐舒适度。',
  },
  {
    title: '山有月茶餐厅',
    imageA: shanyouyue1,
    imageB: shanyouyue2,
    industry: '茶饮简餐',
    area: '约 220㎡',
    duration: '工期 45 天',
    desc: '茶餐厅氛围与灯光层次落地，卡座与过道尺度兼顾私密与翻台，呈现温馨待客场景。',
  },
  {
    title: '福状元 · 洛阳分店',
    imageA: fzyLuoyang1,
    imageB: fzyLuoyang2,
    industry: '餐饮',
    area: '约 240㎡',
    duration: '工期 46 天',
    desc: '洛阳分店空间与总部形象统一，门头识别与室内主材选型可控，保障异地复制效率。',
  },
  {
    title: '杨掌柜辣椒炒肉 · 太康二路店',
    imageA: yangzhanggui1,
    imageB: yangzhanggui2,
    industry: '中式正餐',
    area: '约 150㎡',
    duration: '工期 40 天',
    desc: '太康二路热炒门店重油烟与明厨展示并重，排风与灯光配合菜品呈现，提升就餐区舒适度。',
  },
  {
    title: '福状元 · 平顶山分店',
    imageA: fzyPingdingshan1,
    imageB: fzyPingdingshan2,
    industry: '餐饮',
    area: '约 230㎡',
    duration: '工期 44 天',
    desc: '平顶山门店从门头到就餐区一体化交付，材质与工艺与品牌手册对齐，便于后期运维。',
  },
  {
    title: '河南财经政法大学 · 食堂改造',
    imageA: caida1,
    imageB: caida2,
    industry: '大众食堂',
    area: '约 900㎡',
    duration: '工期 72 天',
    desc: '高校食堂档口与就餐大厅分区明确，人流线与取餐动线优化，满足集中就餐高峰。',
  },
  {
    title: '福状元 · 英协路店',
    imageA: fzyYingxie1,
    imageB: fzyYingxie2,
    industry: '餐饮',
    area: '约 210㎡',
    duration: '工期 40 天',
    desc: '郑州英协路临街店招与室内统一设计语言，前场展示与后场备餐分区合理，保障出餐效率。',
  },
  {
    title: '精品茶舍空间',
    imageA: tea1,
    imageB: tea2,
    industry: '茶空间',
    area: '约 170㎡',
    duration: '工期 35 天',
    desc: '茶舍静谧氛围与展陈结合，照明与材质突出茶品陈列，兼顾品茗与社交场景。',
  },
  {
    title: '福状元 · 索凌路店',
    imageA: fzySuoling1,
    imageB: fzySuoling2,
    industry: '餐饮',
    area: '约 225㎡',
    duration: '工期 43 天',
    desc: '郑州索凌路门店从门头到室内完整落地，桌椅与灯光匹配品牌调性，交付即可开业。',
  },
] as const
</script>

<style scoped>
.store-page {
  min-height: 100dvh;
  background: #f4f4f4;
  color: #000;
}

.store-page__navbg {
  background: #000;
}

.store-page__main {
  padding: 1rem 0 3.6rem;
}

.store-page__main > section {
  opacity: 0;
  transform: translateY(14px);
  animation: section-fade-in 0.6s ease forwards;
}

.store-page__main > section:nth-child(1) { animation-delay: 0.04s; }
.store-page__main > section:nth-child(2) { animation-delay: 0.1s; }
.store-page__main > section:nth-child(3) { animation-delay: 0.16s; }
.store-page__main > section:nth-child(4) { animation-delay: 0.22s; }
.store-page__main > section:nth-child(5) { animation-delay: 0.28s; }
.store-page__main > section:nth-child(6) { animation-delay: 0.34s; }

.store-wrap {
  width: 100%;
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

.store-hero {
  padding: 1.4rem 0 1.9rem;
}

.store-hero__inner {
  border-radius: 24px;
  padding: 2.1rem;
  background: linear-gradient(145deg, #0f0f0f 0%, #262626 100%);
  color: #fff;
}

.store-hero__kicker {
  margin: 0;
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
}

.store-hero__title {
  margin: 0.65rem 0 0;
  font-size: clamp(1.8rem, 3vw + 0.8rem, 2.9rem);
  line-height: 1.15;
  letter-spacing: -0.03em;
}

.store-hero__desc {
  max-width: 48rem;
  margin: 0.9rem 0 0;
  font-size: 1.02rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.84);
}

.store-hero__actions {
  display: flex;
  gap: 12px;
  margin-top: 1.4rem;
  flex-wrap: wrap;
}

.store-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  transition: transform 0.18s ease;
}

.store-btn:hover {
  transform: translateY(-1px);
}

.store-btn--primary {
  background: #fff;
  color: #111;
}

.store-btn--ghost {
  border: 1px solid rgba(255, 255, 255, 0.36);
  color: #fff;
}

.store-section__title {
  margin: 0;
  font-size: clamp(1.4rem, 2.3vw, 2rem);
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.store-highlights {
  padding: 1.8rem 0 1.2rem;
}

.store-highlights__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.store-highlights__grid .store-section__title {
  grid-column: 1 / -1;
}

.store-highlight-card {
  border-radius: 16px;
  padding: 22px 16px 23px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #fff;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.04);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease;
}

.store-highlight-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.12);
}

.store-highlight-card__title {
  margin: 0;
  font-size: 1.04rem;
  font-weight: 800;
}

.store-highlight-card__text {
  margin: 0.55rem 0 0;
  font-size: 0.92rem;
  line-height: 1.65;
  color: rgba(0, 0, 0, 0.74);
}

.store-process {
  padding: 1.9rem 0 1.4rem;
}

.store-process__list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 1rem;
}

.store-process-item {
  padding: 10px 2px 8px;
  border-top: 2px solid rgba(0, 0, 0, 0.16);
}

.store-process-item__index {
  display: inline-block;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  color: rgba(0, 0, 0, 0.5);
  font-weight: 800;
}

.store-process-item__title {
  margin: 0.5rem 0 0;
  font-size: 1.03rem;
  line-height: 1.28;
}

.store-process-item__desc {
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  line-height: 1.62;
  color: rgba(0, 0, 0, 0.72);
}

.store-pricing {
  padding: 1.8rem 0 2rem;
}

.store-pricing__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 1rem;
}

.store-price-card {
  border-radius: 16px;
  padding: 22px 16px 23px;
  background: linear-gradient(180deg, #fff 0%, #f9f9f9 100%);
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease;
}

.store-price-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.12);
}

.store-price-card__label {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.55);
}

.store-price-card__range {
  margin: 0.35rem 0 0;
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.store-price-card__hint {
  margin: 0.55rem 0 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.72);
}

.store-cases {
  padding: 2rem 0 1.6rem;
}

.store-case-grid {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.store-case-card {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #fff;
}

.store-case-card__media {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  padding: 6px;
}

.store-case-card__img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.store-case-card__body {
  padding: 16px 14px 18px;
}

.store-case-card__title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  line-height: 1.3;
}

.store-case-card__meta {
  margin-top: 0.4rem;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.78rem;
  color: rgba(0, 0, 0, 0.55);
}

.store-case-card__desc {
  margin: 0.55rem 0 0;
  font-size: 0.9rem;
  line-height: 1.62;
  color: rgba(0, 0, 0, 0.74);
}

.store-cta {
  padding: 2rem 0 0.8rem;
}

.store-cta__inner {
  border-radius: 22px;
  padding: 1.8rem;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  text-align: center;
}

.store-cta__title {
  margin: 0;
  font-size: clamp(1.3rem, 2vw, 1.8rem);
}

.store-cta__desc {
  margin: 0.55rem auto 0;
  max-width: 40rem;
  color: rgba(0, 0, 0, 0.68);
  line-height: 1.65;
}

.store-cta .store-btn--cta {
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

.store-cta .store-btn--cta:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

@media (max-width: 980px) and (min-width: 768px) {
  .store-highlights__grid,
  .store-process__list,
  .store-pricing__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .store-highlights__grid .store-section__title {
    grid-column: 1 / -1;
  }

  .store-case-grid {
    grid-template-columns: 1fr;
  }

  .store-hero {
    padding: 1.8rem 0 2.1rem;
  }

  .store-hero__inner {
    padding: 1rem 1.35rem 1.5rem !important;
  }

  .store-hero__kicker {
    padding-top: 0.3rem;
  }

  .store-hero__title {
    margin-top: 0.9rem;
  }

  .store-hero__actions {
    margin-top: 1.7rem;
  }

  .store-wrap {
    padding: 0 1.25rem;
  }
}

@media (max-width: 767px) {
  .store-highlights__grid,
  .store-process__list,
  .store-pricing__grid,
  .store-case-grid {
    grid-template-columns: 1fr;
  }

  .store-hero {
    padding: 1.9rem 0 2.2rem;
  }

  .store-hero__inner {
    padding: 0.5rem 1.1rem 1rem !important;
  }

  .store-hero__kicker {
    padding-top: 0.35rem;
  }

  .store-hero__title {
    margin-top: 0.85rem;
  }

  .store-hero__actions {
    margin-top: 1.75rem;
  }

  .store-wrap {
    padding: 0 1rem;
  }

  .store-case-card__img {
    height: 168px;
  }

  .store-cta__inner {
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
  .store-page__main > section {
    opacity: 1;
    transform: none;
    animation: none;
  }

  .store-highlight-card,
  .store-price-card {
    transition: none;
  }

  .store-highlight-card:hover,
  .store-price-card:hover {
    transform: none;
  }
}
</style>

