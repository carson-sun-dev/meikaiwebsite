<template>
  <div class="home-page">
    <HomeSectionFade appear-immediately>
      <HomeHeroSection @quote-search="onHeroQuoteSearch" />
    </HomeSectionFade>

    <HomeSectionFade>
      <CompanyIntro />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeWhySection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeGallerySection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeBusinessDetailsSection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeCtaSection @quote-click="onHeroQuoteSearch" />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomePricingSection />
    </HomeSectionFade>

    <HomeSectionFade>
      <HomeFooter />
    </HomeSectionFade>
  </div>
</template>

<script setup lang="ts">
import CompanyIntro from '@/components/home/CompanyIntro.vue'
import HomeCtaSection from '@/components/home/HomeCtaSection.vue'
import HomeBusinessDetailsSection from '@/components/home/HomeBusinessDetailsSection.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'
import HomeGallerySection from '@/components/home/HomeGallerySection.vue'
import HomeHeroSection from '@/components/home/HomeHeroSection.vue'
import HomePricingSection from '@/components/home/HomePricingSection.vue'
import HomeSectionFade from '@/components/home/HomeSectionFade.vue'
import HomeWhySection from '@/components/home/HomeWhySection.vue'
import './home-page.css'

function onHeroQuoteSearch() {
  /* TODO: 跳转店铺装修报价等 */
}
</script>