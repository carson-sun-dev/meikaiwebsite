<template>
  <section class="home-date-cta-wrap">
    <div class="home-date-cta">
      <div class="home-date-cta__bg" aria-hidden="true">
        <img :src="bgImg" alt="" class="home-date-cta__img" />
        <div class="home-date-cta__overlay" />
      </div>
      <div class="home-date-cta__inner">
        <div class="home-date-cta__text">
          <h2 class="home-date-cta__title">请让我们了解您的需求：</h2>
          <h3 class="home-date-cta__subtitle">{{ scheduleYear }} 工程排期已开启，先到先得！</h3>
          <button type="button" class="home-date-cta__action" @click="onQuoteClick">
            <PaperPlaneIcon class="home-date-cta__icon" />
            <span class="home-date-cta__action-label">一键估价</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import bgImg from '@/source/homepage/4/1.jpg'
import { getCurrentYear } from '@/utils/companyTimeline'

const scheduleYear = getCurrentYear()

const emit = defineEmits<{
  quoteClick: []
}>()

function onQuoteClick() {
  emit('quoteClick')
}
</script>

<style scoped>
/* 与首页 1080 栏、Gallery / 业务细节对齐 */
.home-date-cta-wrap {
  padding-top: 3rem;
  padding-bottom: 3rem;
  padding-inline: max(1.5rem, calc((100vw - 67.5rem) / 2));
  box-sizing: border-box;
}

/* Figma Date section：圆角 20px，内容区约 1080×560，文案与按钮靠左上 */
.home-date-cta {
  position: relative;
  overflow: hidden;
  max-width: 67.5rem;
  min-height: 38.5rem;
  margin-left: auto;
  margin-right: auto;
  border-radius: 20px;
}

.home-date-cta__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
}

.home-date-cta__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.home-date-cta__overlay {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: rgb(0 0 0 / 0.2);
}

.home-date-cta__inner {
  position: relative;
  z-index: 1;
  box-sizing: border-box;
  display: flex;
  min-height: inherit;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  /* Figma: pt 36px px 24px；底部留白用 min-height 撑开图区，避免 pb 320px 过长 */
  padding: 36px 24px 48px;
}

.home-date-cta__text {
  display: flex;
  width: 100%;
  max-width: 69.875rem;
  flex-direction: column;
  align-items: flex-start;
  /* Figma Text gap 31px */
  gap: 31px;
}

/* Figma: Inter Medium 36px */
.home-date-cta__title {
  margin: 0;
  max-width: 100%;
  font-family: Inter, 'Noto Sans JP', 'Noto Sans SC', system-ui, sans-serif;
  font-size: clamp(1.5rem, 4vw, 2.25rem);
  font-weight: 500;
  font-style: normal;
  line-height: normal;
  color: #fff;
}

/* Figma: EB Garamond 48px，tracking -0.96px */
.home-date-cta__subtitle {
  margin: 0;
  max-width: 100%;
  font-family: 'EB Garamond', 'Noto Sans SC', serif;
  font-size: clamp(1.75rem, 5vw, 3rem);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #fff;
}

/* Figma Frame：w 128px，gap 5px，py 10px px 20px，rounded 32px，#ff5449 */
.home-date-cta__action {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  gap: 5px;
  width: 128px;
  padding: 10px 20px;
  border: none;
  border-radius: 32px;
  background: #ff5449;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.home-date-cta__action:hover {
  opacity: 0.94;
}

.home-date-cta__action:active {
  transform: scale(0.98);
}

.home-date-cta__icon {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
  color: #fff;
  transform: translateY(0.5px);
}

.home-date-cta__action-label {
  font-family: Inter, 'Noto Sans JP', 'Noto Sans SC', system-ui, sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: normal;
  white-space: nowrap;
  color: #fff;
}

@media (max-width: 767px) {
  .home-date-cta-wrap {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-inline: 1rem;
  }

  .home-date-cta {
    min-height: 28rem;
    border-radius: 16px;
  }

  .home-date-cta__inner {
    padding: 1.5rem 1.15rem 2.25rem;
  }

  .home-date-cta__text {
    gap: 1.25rem;
  }
}
</style>
