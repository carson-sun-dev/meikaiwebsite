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
        <section class="about-intro" aria-label="关于美恺装饰">
          <div class="about-wrap">
            <div class="about-intro__grid">
              <div class="about-intro__aside">关于美恺装饰</div>

              <div class="about-intro__main">
                <div class="about-intro__block">
                  <div class="about-intro__h">深耕中原七载，匠心筑造品质标杆</div>
                  <div class="about-intro__p">
                    河南美恺装饰有限公司始创于 2017年 ，是一家集门面房店铺、商务办公楼及精品家庭装饰为一体的综合性装饰企业 。公司业务以郑州为核心，深度覆盖洛阳、开封、驻马店等河南各大城市 。在七年的品牌发展进程中，我们始终不惧行业风雨 ，坚持以客户的装饰意见为核心导向 ，凭借卓越的施工速度与交付质量，在河南装饰市场赢得了广泛的企业好评与深厚的口碑认证 。
                  </div>
                </div>

                <div class="about-intro__block">
                  <div class="about-intro__h">二十年工程积淀，全球直供正品保障</div>
                  <div class="about-intro__p">
                    美恺装饰的核心竞争力源于专业的团队管理，公司总工程师拥有超过 <span class="about-intro__em">20</span> 年的资深装修经验，坚持实施一对一深度对接服务，确保每一项全包工程都能精准落地 。在用料方面，我们严守“大牌用料，全球选材”的准则 ，与立邦、多乐士、三棵树、诺贝尔瓷砖、公牛及老板等全球知名品牌建立深度合作 ，确保所有建材均为正品且环保达标 。我们郑重承诺，以行业领先的技术标准与质保服务 ，为每一位客户铸就非凡的商业与居住空间 。
                  </div>
                </div>

                <router-link class="about-intro__link" to="/contact">点击联系我们</router-link>
              </div>
            </div>
          </div>
        </section>
      </HomeSectionFade>

      <HomeSectionFade>
        <section class="about-milestones" aria-label="企业历程与口碑">
          <div class="about-wrap">
            <div class="about-milestones__stack">
              <div class="milestone milestone--right">
                <div class="milestone__media">
                  <img :src="m1" alt="" class="milestone__img" />
                </div>
                <div class="milestone__glass">
                  <div class="milestone__title">七年之旅</div>
                  <div class="milestone__sub">2017-2026</div>
                  <div class="milestone__text">
                    河南美恺装饰有限公司创办于2017年，至今已有7年，七年过程中我们不惧风雨，始终以客户的装饰意见为第一位，秉持以匠心，铸非凡的信念，已成长为具备门面房店铺、商务办公楼、家庭装饰多样业务为一体的综合公司。
                  </div>
                </div>
              </div>

              <div class="milestone milestone--left">
                <div class="milestone__media">
                  <img :src="m2" alt="" class="milestone__img" />
                </div>
                <div class="milestone__glass milestone__glass--alt">
                  <div class="milestone__title">口碑认证</div>
                  <div class="milestone__text">
                    河南美恺装饰有限公司至今已服务大小企业60+，是河南知名餐饮企业福状元的坚实装饰合作伙伴。业务郑州为核心遍及河南各大城市，如洛阳、开封、驻马店、新郑。施工速度以及质量广受企业好评。
                  </div>
                </div>
              </div>

              <div class="milestone milestone--right">
                <div class="milestone__media">
                  <img :src="m3" alt="" class="milestone__img" />
                </div>
                <div class="milestone__glass">
                  <div class="milestone__title">勇创新高</div>
                  <div class="milestone__sub">2017-2026</div>
                  <div class="milestone__text">
                    从创办至今河南美恺装饰有限公司业务年年攀高，至今以完成门面房店铺交付150+，商务办公装修30+，个人家庭装修200+，施工额持续走高！
                  </div>
                </div>
              </div>
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

import heroImg from '@/source/about/1.jpg'
import m1 from '@/source/homepage/2/1.jpg'
import m2 from '@/source/homepage/2/2.jpg'
import m3 from '@/source/homepage/2/3.jpg'
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

.about-intro {
  padding: 5rem 0;
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
  gap: 20px;
}

.about-intro__block {
  font-size: 24px;
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

.about-intro__em {
  font-weight: 900;
}

.about-intro__link {
  width: fit-content;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.12px;
  text-decoration: underline;
  color: inherit;
  line-height: 1.2;
}

.about-intro__link:hover {
  opacity: 0.85;
}

.about-milestones {
  padding: 2.5rem 0 5rem;
}

.about-milestones__stack {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.milestone {
  position: relative;
  width: 100%;
  border-radius: 30px;
  overflow: hidden;
  padding: 20px 0;
  min-height: 424px;
  background: #f7f7f7;
}

.milestone__media {
  position: absolute;
  top: 20px;
  bottom: 20px;
  right: 40px;
  width: min(714px, 62%);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 10px rgba(0, 0, 0, 0.25);
  background: #fff;
}

.milestone--left .milestone__media {
  left: 40px;
  right: auto;
  width: min(617px, 55%);
}

.milestone__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.milestone__glass {
  position: absolute;
  top: 74px;
  left: 26px;
  width: min(472px, 44%);
  border-radius: 20px;
  padding: 19px 10px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.08));
  backdrop-filter: blur(12.5px);
  box-shadow: 5px 10px 20px rgba(0, 0, 0, 0.25);
}

.milestone--left .milestone__glass {
  left: auto;
  right: 26px;
  top: 97px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.17), rgba(255, 255, 255, 0.04));
}

.milestone__glass::after {
  content: '';
  position: absolute;
  inset: -5px;
  border: 5px solid #fbf1f1;
  border-radius: 25px;
  pointer-events: none;
}

.milestone__title {
  font-weight: 900;
  font-size: 24px;
  line-height: 1.15;
  color: #000;
}

.milestone__sub {
  margin-top: 0.25rem;
  font-weight: 900;
  font-size: 24px;
  line-height: 1.15;
  color: #000;
}

.milestone__text {
  margin-top: 0.6rem;
  font-size: 14px;
  line-height: 1.65;
  color: rgba(0, 0, 0, 0.75);
  font-weight: 700;
}

@media (max-width: 980px) {
  .about-intro__grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .about-intro__aside {
    width: 100%;
  }

  .milestone {
    padding: 20px 0 28px;
    min-height: auto;
  }

  .milestone__media,
  .milestone--left .milestone__media {
    position: relative;
    top: auto;
    left: auto;
    right: auto;
    bottom: auto;
    width: 100%;
    height: 260px;
    margin: 0 auto;
    border-radius: 20px;
    box-shadow: 0 12px 18px rgba(0, 0, 0, 0.18);
  }

  .milestone__glass,
  .milestone--left .milestone__glass {
    position: relative;
    top: auto;
    left: auto;
    right: auto;
    width: 100%;
    margin: 14px auto 0;
  }
}

</style>

