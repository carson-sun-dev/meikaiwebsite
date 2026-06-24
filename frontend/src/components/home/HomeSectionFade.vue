<template>
  <div
    ref="rootEl"
    class="home-section-fade"
    :class="{ 'home-section-fade--visible': visible }"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    /** 首屏区块：挂载后即视为可见，避免先透明再等 IntersectionObserver */
    appearImmediately?: boolean
    /** 进入视口多少比例算作「可见」 */
    threshold?: number
  }>(),
  {
    appearImmediately: false,
    threshold: 0.12,
  },
)

const rootEl = ref<HTMLElement | null>(null)
const visible = ref(props.appearImmediately)
const revealedOnce = ref(props.appearImmediately)

let observer: IntersectionObserver | undefined

function attach() {
  detach()
  if (props.appearImmediately || !rootEl.value) {
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0]
      if (!entry) {
        return
      }
      if (!revealedOnce.value && entry.isIntersecting) {
        visible.value = true
        revealedOnce.value = true
        // 区块首次出现后不再重复触发，避免滚动到临界位置时反复闪动
        detach()
      }
    },
    {
      root: null,
      threshold: props.threshold,
      rootMargin: '0px 0px -6% 0px',
    },
  )
  observer.observe(rootEl.value)
}

function detach() {
  observer?.disconnect()
  observer = undefined
}

onMounted(() => {
  if (props.appearImmediately) {
    visible.value = true
    return
  }
  if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    visible.value = true
    return
  }
  attach()
})

onUnmounted(() => {
  detach()
})
</script>

<style scoped>
/* 用户反馈"滚轮吸附"持续存在 — 直接取消整个淡入逻辑,变成纯包装(2026-06-22)
 * 保留组件外壳便于将来恢复动画,但视觉上节区即来即显,滚动 100% 流畅。 */
.home-section-fade,
.home-section-fade--visible {
  opacity: 1;
  transform: none;
  transition: none;
  will-change: auto;
}
</style>
