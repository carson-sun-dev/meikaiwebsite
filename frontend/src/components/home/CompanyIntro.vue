<template>
  <section class="company-intro">
    <div class="company-intro__grid">
      <div class="company-intro__aside">
        <p class="company-intro__label">公司简介</p>
        <div class="company-intro__lines">
          <span class="company-intro__line-short" />
          <span class="company-intro__line-long" />
        </div>
      </div>
      <div class="company-intro__main">
        <p class="company-intro__text">
          多年深耕，美恺以丰富的装饰经验为基石，致力于为您破解空间难题。用匠心构筑品质环境，以卓越空间您的事业成功！
        </p>
        <router-link class="company-intro__link" to="/about">点击了解更多企业历程</router-link>
      </div>
    </div>
  </section>

    <section class="company-intro-projects">
      <div class="company-intro-projects__inner">
        <div class="company-intro-projects__grid">
          <article class="company-intro-card">
            <div class="company-intro-card__thumb">
              <img :src="Img1" alt="" />
            </div>
            <h3 class="company-intro-card__title">七年之旅</h3>
            <p class="company-intro-card__desc">2017-2026 我们一直在路上</p>
          </article>
          <article class="company-intro-card">
            <div class="company-intro-card__thumb">
              <img :src="Img2" alt="" />
            </div>
            <h3 class="company-intro-card__title">口碑认证</h3>
            <p class="company-intro-card__desc">多家河南知名企业合作伙伴，工程质量广受好评</p>
          </article>
          <article class="company-intro-card">
            <div class="company-intro-card__thumb">
              <img :src="Img3" alt="" />
            </div>
            <h3 class="company-intro-card__title">连创新高</h3>
            <p class="company-intro-card__desc">公司业绩、工程规模持续攀升稳步增长</p>
          </article>
        </div>
      </div>
    </section>
</template>

<script setup lang="ts">
import Img1 from '@/source/homepage/2/1.jpg'
import Img2 from '@/source/homepage/2/2.jpg'
import Img3 from '@/source/homepage/2/3.jpg'
</script>

<style scoped>
.company-intro {
  border-bottom: 1px solid #f5f5f5;
  padding: 5rem 1.5rem;
  color: #000;
}

@media (min-width: 768px) {
  .company-intro {
    padding-top: 5rem;
    padding-bottom: 5rem;
  }
}

.company-intro__grid {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.25rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

@media (min-width: 768px) {
  .company-intro__grid {
    flex-direction: row;
    gap: 15rem;
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.company-intro__aside {
  flex-shrink: 0;
  width: 100%;
}

@media (min-width: 768px) {
  .company-intro__aside {
    width: 11.4375rem;
  }
}

.company-intro__main {
  display: flex;
  min-width: 0;
  flex: 1 0 0;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.25rem;
}

.company-intro__label {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  line-height: 1.2;
  color: #000;
  font-feature-settings: 'lnum' 1, 'tnum' 1;
}

.company-intro__lines {
  margin-top: 1rem;
  display: flex;
  gap: 0.75rem;
}

.company-intro__line-short {
  height: 1px;
  width: 3rem;
  align-self: center;
  background: #d4d4d4;
}

.company-intro__line-long {
  height: 1px;
  flex: 1;
  background: #e5e5e5;
}

.company-intro__text {
  margin: 0;
  width: 100%;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.01em;
  color: #000;
  font-feature-settings: 'lnum' 1, 'tnum' 1;
}

.company-intro__link {
  font-size: 0.75rem;
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: -0.01em;
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 0.15em;
  font-feature-settings: 'lnum' 1, 'tnum' 1;
}

.company-intro__link:hover {
  opacity: 0.85;
}

/* 下方三列项目（原 home-projects） */
.company-intro-projects {
  padding: 5rem 1.5rem;
}

@media (min-width: 768px) {
  .company-intro-projects {
    padding-top: 6rem;
    padding-bottom: 6rem;
  }
}

.company-intro-projects__inner {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

@media (min-width: 768px) {
  .company-intro-projects__inner {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.company-intro-projects__grid {
  display: grid;
  gap: 2rem;
}

@media (min-width: 768px) {
  .company-intro-projects__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.company-intro-card__thumb {
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: 0.75rem;
  background: #f5f5f5;
}

.company-intro-card__thumb img {
  height: 100%;
  width: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.company-intro-card:hover .company-intro-card__thumb img {
  transform: scale(1.05);
}

.company-intro-card__title {
  margin-top: 1.25rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #171717;
}

.company-intro-card__desc {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #737373;
}
</style>
