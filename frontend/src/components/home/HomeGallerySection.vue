<template>
  <section class="mk-section gallery-section" aria-label="精选案例">
    <div class="mk-container">
      <header class="mk-section-header" ref="headerRef" :class="{ 'is-visible': revealedHeader }">
        <span class="mk-eyebrow">Selected Works</span>
        <h2 class="mk-title">精选案例</h2>
        <p class="mk-title-sub">店铺 · 家装· 商务办公  ·  业务线代表作</p>
      </header>

      <div class="gallery-grid">
        <router-link
          v-for="(g, i) in galleryItems"
          :key="g.caption"
          :to="g.route"
          class="gallery-item"
          :class="{ 'is-visible': revealedCards }"
          :style="{ transitionDelay: `${i * 0.08}s`, backgroundImage: `url(${g.img})` }"
        >
          <div class="gallery-item__overlay" aria-hidden="true"></div>
          <div class="gallery-item__caption">
            <div class="gallery-item__eyebrow">{{ g.tag }}</div>
            <div class="gallery-item__title">{{ g.caption }}</div>
          </div>
        </router-link>
      </div>

      <div class="gallery-cta">
        <a href="javascript:void(0)" role="button" class="mk-btn mk-btn--outline" @click="openChat">即刻向客服咨询</a>
      </div>
    </div>
  </section>

  <!-- 节区尾 logo divider -->
  <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
    <span class="mk-divider__seal"></span>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import logoImg from '@/source/logo/logo.webp'
import { useChatWidget } from '@/composables/useChatWidget'

const { open: openChat } = useChatWidget()

// 6 张代表性案例图,3 业务各 2 张;按 demo 风格 3 列 2 行 grid
import imgHouse1 from '@/source/house/2_1.webp'
import imgHouse2 from '@/source/house/5_1.webp'
import imgStore1 from '@/source/store/福状元 商英街1.webp'
import imgStore2 from '@/source/store/茶舍1.webp'
import imgBusiness1 from '@/source/business/b1_1.webp'
import biz2 from '@/source/business/biz2.webp'

const galleryItems = [
  { img: imgStore1,    tag: 'Storefront',  caption: '福状元 · 商英街店',   route: '/store' as const },
  { img: imgHouse1,    tag: 'Residential', caption: '现代精装住宅',         route: '/residential' as const },
  { img: imgBusiness1, tag: 'Office',      caption: '商务办公空间',         route: '/business' as const },
  { img: imgStore2,    tag: 'Storefront',  caption: '茶舍 · 雅集空间',     route: '/store' as const },
  { img: imgHouse2,    tag: 'Residential', caption: '轻奢家装样板',         route: '/residential' as const },
  { img: biz2, tag: 'Office',      caption: '企业办公环境',         route: '/business' as const },
] as const

const headerRef = ref<HTMLElement | null>(null)
const revealedHeader = ref(false)
const revealedCards = ref(false)
let obs: IntersectionObserver | undefined

onMounted(() => {
  if (typeof window === 'undefined') return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealedHeader.value = true
    revealedCards.value = true
    return
  }
  if (!headerRef.value) return
  obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        revealedHeader.value = true
        setTimeout(() => { revealedCards.value = true }, 120)
        obs?.disconnect()
      }
    })
  }, { threshold: 0.15 })
  obs.observe(headerRef.value)
})

onUnmounted(() => obs?.disconnect())
</script>

<style scoped>
.gallery-section { background: var(--mk-paper); }

.mk-section-header {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
@media (max-width: 900px) { .gallery-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .gallery-grid { grid-template-columns: 1fr; } }

.gallery-item {
  position: relative;
  display: block;
  aspect-ratio: 4 / 3;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  overflow: hidden;
  cursor: pointer;
  border-radius: 4px;
  text-decoration: none;
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.gallery-item.is-visible { opacity: 1; transform: translateY(0); }

.gallery-item__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 55%, rgba(0, 0, 0, 0.78) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}
.gallery-item:hover .gallery-item__overlay { opacity: 1; }

.gallery-item__caption {
  position: absolute;
  bottom: 24px;
  left: 24px;
  right: 24px;
  color: white;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.gallery-item:hover .gallery-item__caption {
  opacity: 1;
  transform: translateY(0);
}

.gallery-item__eyebrow {
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 11px;
  letter-spacing: 0.3em;
  opacity: 0.85;
  text-transform: uppercase;
}

.gallery-item__title {
  font-family: var(--mk-font-serif);
  font-size: 18px;
  margin-top: 6px;
  letter-spacing: 0.05em;
}

.gallery-cta {
  text-align: center;
  margin-top: 48px;
}

@media (prefers-reduced-motion: reduce) {
  .gallery-item { opacity: 1; transform: none; transition: none; }
  .gallery-item__overlay, .gallery-item__caption { transition: none; }
}

/* 触摸屏(无 hover):蒙版 + 标题直接显示,不再依赖 hover(避免与点击跳转冲突)
   用 hover:none + pointer:coarse 仅对手机/平板生效,比 max-width 更准 */
@media (hover: none) and (pointer: coarse) {
  .gallery-item__overlay { opacity: 1; }
  .gallery-item__caption { opacity: 1; transform: translateY(0); }
}
</style>
