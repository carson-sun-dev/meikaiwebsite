<template>
  <div class="about-page">
    <main class="about-page__main">
      <HomeSectionFade appear-immediately>
        <section class="about-hero" aria-label="关于我们主视觉">
          <div class="about-hero__nav" aria-hidden="true">
            <NavigationBar />
          </div>
          <img :src="heroImg" alt="" class="about-hero__bg" />
          <div class="about-hero__overlay" aria-hidden="true" />

          <div class="about-hero__content">
            <div class="about-hero__kicker">ABOUT MEIKAI</div>
            <h1 class="about-hero__title">美恺装饰 · 公司介绍</h1>
            <p class="about-hero__desc">
              从设计到施工的每一个节点，我们都以可落地的方案和可验证的工艺，为每一位客户交付更放心的装修结果。
            </p>
          </div>
        </section>
      </HomeSectionFade>

      <HomeSectionFade>
        <section class="about-metrics" aria-label="品牌关键数据">
          <div class="about-wrap">
            <div class="about-metrics__grid">
              <article class="about-metric">
                <div class="about-metric__value">{{ metricYearsPlus }}</div>
                <div class="about-metric__label">河南本地深耕经验</div>
              </article>
              <article class="about-metric">
                <div class="about-metric__value">380+</div>
                <div class="about-metric__label">累计项目交付</div>
              </article>
              <article class="about-metric">
                <div class="about-metric__value">40+</div>
                <div class="about-metric__label">服务企业客户</div>
              </article>
              <article class="about-metric">
                <div class="about-metric__value">30年</div>
                <div class="about-metric__label">总工程师实战经验</div>
              </article>
            </div>
          </div>
        </section>
      </HomeSectionFade>

      <HomeSectionFade>
        <section class="about-intro" aria-label="关于美恺装饰">
          <div class="about-wrap">
            <div class="about-intro__grid">
              <div class="about-intro__aside">关于美恺装饰</div>

              <div class="about-intro__main">
                <div class="about-intro__block">
                  <div class="about-intro__h">深耕中原{{ deepRootZai }}，匠心筑造品质标杆</div>
                  <ul class="about-intro__list">
                    <li>始于 {{ foundedYear }} 年，聚焦店铺、商务办公、精品家装三大场景。</li>
                    <li>以郑州为核心，服务覆盖洛阳、开封、驻马店等河南多地。</li>
                    <li>坚持“方案可落地、工艺可验证、交付可追踪”的项目管理标准。</li>
                  </ul>
                </div>

                <div class="about-intro__block">
                  <div class="about-intro__h">三十年工程积淀，全球直供正品保障</div>
                  <ul class="about-intro__list">
                    <li>总工程师团队具备 <span class="about-intro__em">30</span> 年以上施工与管理经验。</li>
                    <li>采用一对一深度对接机制，确保关键节点沟通透明。</li>
                    <li>与立邦、多乐士、三棵树、诺贝尔、公牛、老板等品牌合作，保障正品与环保标准。</li>
                  </ul>
                </div>

                <div class="about-intro__cta">
                  <router-link class="about-intro__btn about-intro__btn--primary" to="/contact">30秒获取装修报价</router-link>
                  <router-link class="about-intro__btn about-intro__btn--ghost" to="/store">查看品牌店装案例</router-link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </HomeSectionFade>

      <HomeSectionFade>
        <section class="about-milestones" aria-label="企业历程与口碑">
          <div class="about-wrap">
            <div class="about-milestones__head">
              <p class="about-milestones__kicker">MEIKAI TIMELINE</p>
              <h2 class="about-milestones__title">从创立到规模化交付的三次跨越</h2>
            </div>

            <div class="about-timeline">
              <article class="timeline-item">
                <div class="timeline-item__track" aria-hidden="true">
                  <span class="timeline-item__dot" />
                </div>
                <div class="timeline-item__period">{{ foundedYear }} - 2020</div>
                <div class="timeline-item__card">
                  <div class="timeline-item__content">
                    <h3 class="timeline-item__title">品牌创立与标准搭建</h3>
                    <p class="timeline-item__text">
                      公司创立后快速建立设计、施工、交付协同机制，形成覆盖店铺、商务办公与家庭装饰的标准化服务流程。
                    </p>
                  </div>
                  <div class="timeline-item__media">
                    <img :src="m1" alt="" class="timeline-item__img" />
                  </div>
                </div>
              </article>

              <article class="timeline-item">
                <div class="timeline-item__track" aria-hidden="true">
                  <span class="timeline-item__dot" />
                </div>
                <div class="timeline-item__period">2021 - 2024</div>
                <div class="timeline-item__card">
                  <div class="timeline-item__content">
                    <h3 class="timeline-item__title">口碑沉淀与区域扩张</h3>
                    <p class="timeline-item__text">
                      持续服务河南多地客户，累计企业合作 60+，并与多家标杆餐饮品牌建立长期合作关系，交付质量与效率获得广泛认可。
                    </p>
                  </div>
                  <div class="timeline-item__media">
                    <img :src="m2" alt="" class="timeline-item__img" />
                  </div>
                </div>
              </article>

              <article class="timeline-item">
                <div class="timeline-item__track" aria-hidden="true">
                  <span class="timeline-item__dot" />
                </div>
                <div class="timeline-item__period">2025 - 至今</div>
                <div class="timeline-item__card">
                  <div class="timeline-item__content">
                    <h3 class="timeline-item__title">规模增长与能力进阶</h3>
                    <p class="timeline-item__text">
                      累计实现店铺交付 150+、商务办公 30+、家庭装修 200+，并持续优化工程管理体系，实现项目规模与品质的双增长。
                    </p>
                  </div>
                  <div class="timeline-item__media">
                    <img :src="m3" alt="" class="timeline-item__img" />
                  </div>
                </div>
              </article>
            </div>
          </div>
        </section>
      </HomeSectionFade>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'
import HomeSectionFade from '@/components/home/HomeSectionFade.vue'

import heroImg from '@/source/about/1.webp'
import m1 from '@/source/about/2/1.webp'
import m2 from '@/source/about/2/2.webp'
import m3 from '@/source/about/2/3.webp'
import { COMPANY_FOUNDED_YEAR, getMetricYearsPlus, getZhYearsZaiPhrase } from '@/utils/companyTimeline'

const metricYearsPlus = getMetricYearsPlus()
const deepRootZai = getZhYearsZaiPhrase()
const foundedYear = COMPANY_FOUNDED_YEAR
</script>

<style scoped>
.about-page {
  min-height: 100dvh;
  background: #fff;
  color: #000;
}

.about-page__main {
  padding: 0 0 2.5rem;
}

.about-hero {
  position: relative;
  overflow: hidden;
  height: 100dvh;
}

.about-hero__nav {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 20;
  background: transparent;
}

.about-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-hero__overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
}

.about-hero__content {
  position: relative;
  z-index: 1;
  height: 100%;
  max-width: 67.5rem;
  margin: 0 auto;
  padding: 88px 1.5rem 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  box-sizing: border-box;
}

.about-hero__kicker {
  font-weight: 800;
  letter-spacing: 0.12em;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.85);
}

.about-hero__title {
  margin: 0;
  font-size: clamp(2rem, 4vw + 1rem, 3.25rem);
  font-weight: 900;
  letter-spacing: -0.03em;
  color: rgba(255, 255, 255, 0.96);
}

.about-hero__desc {
  margin: 0;
  max-width: 40rem;
  font-size: 1rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.82);
}

.about-wrap {
  width: 100%;
  max-width: 67.5rem;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

.about-metrics {
  padding: 4.5rem 0 1rem;
}

.about-metrics__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.about-metric {
  border-radius: 16px;
  padding: 20px 18px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #fff 0%, #f9f9f9 100%);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease;
}

.about-metric:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 38px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.12);
}

.about-metric__value {
  font-size: clamp(1.6rem, 2.4vw, 2.1rem);
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.about-metric__label {
  margin-top: 8px;
  font-size: 0.92rem;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.66);
}

.about-intro {
  padding: 4rem 0 5.5rem;
}

.about-intro__grid {
  display: grid;
  grid-template-columns: 183px 1fr;
  gap: clamp(2.5rem, 12vw, 240px);
  align-items: flex-start;
  color: #000;
}

.about-intro__aside {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.24px;
}

.about-intro__main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.about-intro__block {
  font-size: 20px;
  font-feature-settings: 'lnum' 1, 'tnum' 1;
}

.about-intro__h {
  font-weight: 800;
  letter-spacing: 0.24px;
  line-height: 1.3;
}

.about-intro__p {
  margin-top: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.16px;
  line-height: 1.3;
  color: rgba(0, 0, 0, 0.78);
}

.about-intro__list {
  margin: 0.8rem 0 0;
  padding-left: 1.15rem;
  display: grid;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.7;
  color: rgba(0, 0, 0, 0.8);
}

.about-intro__em {
  font-weight: 900;
}

.about-intro__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.about-intro__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
  text-decoration: none;
  transition: transform 0.18s ease;
}

.about-intro__btn:hover {
  transform: translateY(-1px);
}

.about-intro__btn--primary {
  background: #111;
  color: #fff;
}

.about-intro__btn--ghost {
  color: #111;
  border: 1px solid rgba(0, 0, 0, 0.22);
  background: #fff;
}

.about-milestones {
  padding: 1.5rem 0 5rem;
}

.about-milestones__head {
  margin-bottom: 1.4rem;
}

.about-milestones__kicker {
  margin: 0;
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.48);
}

.about-milestones__title {
  margin: 0.45rem 0 0;
  font-size: clamp(1.4rem, 2.4vw, 2rem);
  line-height: 1.28;
  letter-spacing: -0.02em;
}

.about-timeline {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.timeline-item {
  position: relative;
  display: grid;
  grid-template-columns: 22px 140px 1fr;
  align-items: stretch;
  gap: 16px;
}

.timeline-item__track {
  position: relative;
}

.timeline-item__track::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: -16px;
  width: 2px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.25) 0%, rgba(0, 0, 0, 0.08) 100%);
}

.timeline-item:last-child .timeline-item__track::before {
  bottom: 0;
}

.timeline-item__dot {
  position: absolute;
  left: 4px;
  top: 20px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #111;
  box-shadow: 0 0 0 4px rgba(17, 17, 17, 0.12);
}

.timeline-item__period {
  padding-top: 16px;
  font-size: 0.9rem;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.58);
}

.timeline-item__card {
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #fff 0%, #f8f8f8 100%);
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 18px;
  padding: 18px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease;
}

.timeline-item__card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 44px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.12);
}

.timeline-item__card:hover .timeline-item__img {
  transform: scale(1.03);
}

.timeline-item__content {
  min-width: 0;
}

.timeline-item__title {
  margin: 0;
  font-size: clamp(1.05rem, 1.4vw, 1.3rem);
  line-height: 1.3;
  font-weight: 800;
  letter-spacing: 0.01em;
}

.timeline-item__text {
  margin: 0.55rem 0 0;
  font-size: 0.95rem;
  line-height: 1.72;
  color: rgba(0, 0, 0, 0.72);
}

.timeline-item__media {
  border-radius: 14px;
  overflow: hidden;
  height: 180px;
  background: #fff;
  box-shadow: 0 10px 18px rgba(0, 0, 0, 0.14);
}

.timeline-item__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.35s ease;
}

@media (max-width: 767px) {
  .about-hero {
    height: auto;
    min-height: 100dvh;
  }

  .about-hero__content {
    min-height: 100dvh;
    padding: 5.5rem 1.15rem 3.5rem;
    align-items: flex-start;
    text-align: left;
  }

  .about-hero__desc {
    max-width: 34rem;
  }

  .about-wrap {
    padding: 0 1.15rem;
  }
}

@media (max-width: 980px) {
  .about-metrics {
    padding-top: 3.25rem;
  }

  .about-metrics__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .about-intro__grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .about-intro__aside {
    width: 100%;
  }

  .about-intro__block {
    font-size: 18px;
    padding: 14px 14px 12px;
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    background: linear-gradient(180deg, #fff 0%, #fafafa 100%);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.04);
  }

  .timeline-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .timeline-item__track {
    display: none;
  }

  .timeline-item__period {
    padding-top: 0;
  }

  .timeline-item__card {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .timeline-item__media {
    height: 220px;
  }
}

@media (max-width: 640px) {
  .about-metrics__grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .about-metric,
  .timeline-item__card {
    transition: none;
  }

  .about-metric:hover,
  .timeline-item__card:hover {
    transform: none;
  }

  .timeline-item__img {
    transition: none;
  }

  .timeline-item__card:hover .timeline-item__img {
    transform: none;
  }
}

</style>

