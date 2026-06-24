<template>
  <section class="mk-section process-section" aria-label="从咨询到交付的服务流程">
    <div class="mk-container">
      <header class="mk-section-header" ref="headerRef" :class="{ 'is-visible': revealedHeader }">
        <span class="mk-eyebrow">Our Process</span>
        <h2 class="mk-title">从咨询到交付，四步走完</h2>
        <p class="mk-title-sub">让您清楚知道每个节点正在做什么</p>
      </header>

      <div class="process-flow">
        <div
          v-for="(s, i) in steps"
          :key="s.no"
          class="process-step"
          :class="{ 'is-visible': revealedSteps }"
          :style="{ transitionDelay: `${i * 0.1}s` }"
        >
          <div class="process-step__num">{{ s.no }}</div>
          <h4 class="process-step__title">{{ s.title }}</h4>
          <p class="process-step__desc">{{ s.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 尾部 logo 分隔器 -->
  <div class="mk-divider" :style="{ '--mk-divider-logo': `url(${logoImg})` }">
    <span class="mk-divider__seal"></span>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import logoImg from '@/source/logo/logo.webp'

// 节点繁体数字(壹贰叁肆) 按用户决策保留;其余文案全简体
const steps = [
  { no: '壹', title: '需求沟通', desc: '确认装修目标、风格偏好与预算范围，让方案从源头更准确。' },
  { no: '贰', title: '方案设计', desc: '提供可落地的设计与结构说明，并配合关键节点的对齐确认。' },
  { no: '叁', title: '施工实施', desc: '用工艺标准推进每一道工序，保证质量与进度可视化。' },
  { no: '肆', title: '验收交付', desc: '完成细节收口与整体复核，让结果一次到位更省心。' },
] as const

const headerRef = ref<HTMLElement | null>(null)
const revealedHeader = ref(false)
const revealedSteps = ref(false)
let obs: IntersectionObserver | undefined

onMounted(() => {
  if (typeof window === 'undefined') return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealedHeader.value = true
    revealedSteps.value = true
    return
  }
  if (!headerRef.value) return
  obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        revealedHeader.value = true
        setTimeout(() => { revealedSteps.value = true }, 120)
        obs?.disconnect()
      }
    })
  }, { threshold: 0.15 })
  obs.observe(headerRef.value)
})

onUnmounted(() => obs?.disconnect())
</script>

<style scoped>
.process-section { background: var(--mk-paper-pure); }

.mk-section-header {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.8s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.mk-section-header.is-visible { opacity: 1; transform: translateY(0); }

.process-flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  position: relative;
}
.process-flow::before {
  content: '';
  position: absolute;
  top: 38px; /* 圆章中心线 */
  left: 12%;
  right: 12%;
  height: 1px;
  background: var(--mk-gold-soft);
  z-index: 0;
}
@media (max-width: 768px) {
  .process-flow { grid-template-columns: repeat(2, 1fr); gap: 40px 0; }
  .process-flow::before { display: none; }
}

.process-step {
  text-align: center;
  padding: 0 16px;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.2, 0.7, 0.2, 1),
              transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.process-step.is-visible { opacity: 1; transform: translateY(0); }

.process-step__num {
  width: 76px;
  height: 76px;
  margin: 0 auto 22px;
  background: white;
  border: 2px solid var(--mk-brand);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mk-font-serif);
  font-size: 30px;
  color: var(--mk-brand);
  transition: all 0.4s cubic-bezier(0.2, 0.85, 0.3, 1.05);
}
.process-step:hover .process-step__num {
  background: var(--mk-brand);
  color: white;
  transform: scale(1.08);
  box-shadow: var(--mk-shadow-brand);
}

.process-step__title {
  font-family: var(--mk-font-serif);
  font-size: 18px;
  font-weight: 500;
  color: var(--mk-ink);
  margin: 0 0 10px;
  letter-spacing: 0.06em;
}

.process-step__desc {
  margin: 0;
  font-size: 13px;
  color: var(--mk-ink-3);
  line-height: 1.75;
}

@media (prefers-reduced-motion: reduce) {
  .process-step { opacity: 1; transform: none; transition: none; }
  .process-step:hover .process-step__num { transform: none; }
}

/* divider 背景跟 Process 节区同色(--mk-paper-pure),视觉上挂在 Process 底部,
   不再被下一节 Gallery 的米灰(--mk-paper)同色"吸"过去显得像 Gallery 顶部 */
.mk-divider { background: var(--mk-paper-pure); }
</style>
