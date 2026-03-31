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
      visible.value = entry.isIntersecting
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
.home-section-fade {
  opacity: 0;
  transform: translateY(2rem);
  transition:
    opacity 1s cubic-bezier(0.22, 1, 0.36, 1),
    transform 1s cubic-bezier(0.22, 1, 0.36, 1);
  will-change: opacity, transform;
}

.home-section-fade--visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .home-section-fade {
    opacity: 1;
    transform: none;
    transition: none;
    will-change: auto;
  }
}
</style>
