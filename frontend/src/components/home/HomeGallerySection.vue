<template>
  <section class="home-gallery">
    <div class="home-gallery__stack">
      <div class="home-gallery__text-block">
        <h2 class="home-gallery__section-label">装修案例</h2>
        <div class="home-gallery__intro">
          <h3 class="home-gallery__display-title">体验我们的成果</h3>
          <router-link to="/contact" class="home-gallery__contact-link">立刻联系</router-link>
        </div>
      </div>
    </div>

    <HomeGalleryMarqueeStrip :items="homeGalleryMarqueeItems" />
  </section>
</template>

<script setup lang="ts">
import HomeGalleryMarqueeStrip from '@/components/home/HomeGalleryMarqueeStrip.vue'
import { homeGalleryMarqueeItems } from '@/data/homeGalleryMarqueeItems'
</script>
