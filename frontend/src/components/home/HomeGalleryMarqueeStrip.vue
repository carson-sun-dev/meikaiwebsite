<template>
  <div class="home-gallery__marquee-shell" aria-label="案例图片展示">
    <div class="home-gallery__marquee">
      <div class="home-gallery__marquee-track">
        <template v-for="dup in [0, 1]" :key="`dup-${dup}`">
          <div
            v-for="(group, gi) in groups"
            :key="`dup-${dup}-g-${gi}`"
            class="home-gallery__group"
          >
            <div
              v-for="item in group"
              :key="`dup-${dup}-${item.id}`"
              :class="itemClasses(item)"
            >
              <div class="home-gallery__marquee-img-wrap">
                <img :src="item.image" :alt="item.caption" loading="lazy" />
              </div>
              <p class="home-gallery__marquee-caption">{{ item.caption }}</p>
            </div>
          </div>
        </template>
      </div>
    </div>
    <div class="home-gallery__marquee-indicator" aria-hidden="true" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { HomeGallerySlideItem } from '@/data/homeGalleryMarqueeItems'

const props = defineProps<{
  items: HomeGallerySlideItem[]
}>()

function chunkItems(items: HomeGallerySlideItem[], size: number): HomeGallerySlideItem[][] {
  const out: HomeGallerySlideItem[][] = []
  for (let i = 0; i < items.length; i += size) {
    out.push(items.slice(i, i + size))
  }
  return out
}

const groups = computed(() => chunkItems(props.items, 3))

function itemClasses(item: HomeGallerySlideItem) {
  const classes = [
    'home-gallery__marquee-item',
    `home-gallery__marquee-item--${item.size}`,
  ]
  const v = item.variant
  if (v && v !== 'default') {
    classes.push(`home-gallery__marquee-item--${v}`)
  }
  return classes
}
</script>
