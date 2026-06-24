<template>
  <div class="home-page">
    <!-- HeroQuoteSearchPill 点击行为已由 useChatWidget 接管(2026-06-22),不再 emit quoteSearch -->
    <HomeHeroSection />

    <!-- Stats 紧贴 hero 下方:深耕年/项目/装修团队/回访 — 不入 SectionFade 让数据立即显 -->
    <HomeStatsSection />

    <HomeSectionFade>
      <CompanyIntro />
    </HomeSectionFade>

    <!-- Why:不带尾 divider(按用户决策"为什么选择美恺这里就不在该部分") -->
    <HomeSectionFade>
      <HomeWhySection />
    </HomeSectionFade>

    <!-- Business / Process / Gallery / Pricing 各自模板内已带尾 divider -->
    <HomeSectionFade>
      <HomeBusinessDetailsSection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeProcessSection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeGallerySection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomePricingSection />
    </HomeSectionFade>

    <!-- HomeCtaSection 移除(用户反馈):转化入口已由 footer 的"保持联系"+ 右下角 ChatFab 承担 -->

    <HomeSectionFade>
      <HomeFooter />
    </HomeSectionFade>
  </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
import CompanyIntro from '@/components/home/CompanyIntro.vue'
import HomeHeroSection from '@/components/home/HomeHeroSection.vue'
import HomeSectionFade from '@/components/home/HomeSectionFade.vue'
import HomeStatsSection from '@/components/home/HomeStatsSection.vue'
import './home-page.css'

const HomeWhySection = defineAsyncComponent(() => import('@/components/home/HomeWhySection.vue'))
const HomeBusinessDetailsSection = defineAsyncComponent(
  () => import('@/components/home/HomeBusinessDetailsSection.vue'),
)
const HomeProcessSection = defineAsyncComponent(() => import('@/components/home/HomeProcessSection.vue'))
const HomeGallerySection = defineAsyncComponent(() => import('@/components/home/HomeGallerySection.vue'))
const HomePricingSection = defineAsyncComponent(() => import('@/components/home/HomePricingSection.vue'))
const HomeFooter = defineAsyncComponent(() => import('@/components/home/HomeFooter.vue'))
</script>
