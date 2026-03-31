<!-- 玻璃条：文案与 Hero 全屏轮播同一 tick 切换；动画仍为上移淡出 + 下方滚入 -->
<template>
  <div class="quote-pill">
    <button type="button" class="quote-pill__arrow-frame" aria-label="查看报价" @click="emit('search')">
      <el-icon :size="14" class="quote-pill__arrow-icon"><TopRight /></el-icon>
    </button>
    <span class="quote-pill__divider" aria-hidden="true" />
    <div class="quote-pill__text-slot">
      <Transition name="quote-text" mode="out-in">
        <p :key="activeIndex" class="quote-pill__text">{{ currentText }}</p>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TopRight } from '@element-plus/icons-vue'

const props = defineProps<{
  messages: readonly string[]
  activeIndex: number
}>()

const emit = defineEmits<{
  search: []
}>()

const currentText = computed(() => {
  const len = props.messages.length
  if (len === 0) {
    return ''
  }
  const i = ((props.activeIndex % len) + len) % len
  return props.messages[i] ?? ''
})
</script>

<style scoped>
.quote-pill {
  position: relative;
  isolation: isolate;
  display: flex;
  box-sizing: border-box;
  width: fit-content;
  min-width: 260px;
  max-width: min(92vw, 34ch);
  height: 37px;
  align-items: center;
  gap: 6px;
  padding: 2px 9px;
  border-radius: 15px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(1px);
  -webkit-backdrop-filter: blur(4px);
}

.quote-pill::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(
    150deg,
    rgba(255, 255, 255, 0.95) 0%,
    rgba(255, 255, 255, 0.45) 22%,
    rgba(255, 255, 255, 0.18) 45%,
    rgba(255, 255, 255, 0.12) 65%,
    rgba(255, 255, 255, 0.08) 100%
  );
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
  z-index: 0;
}

.quote-pill::after {
  content: '';
  position: absolute;
  inset: 1px;
  border-radius: 14px;
  pointer-events: none;
  box-shadow: inset 1px 1px 0 rgba(255, 255, 255, 0.35);
  z-index: 0;
}

.quote-pill__arrow-frame,
.quote-pill__divider,
.quote-pill__text-slot {
  position: relative;
  z-index: 1;
}

.quote-pill__arrow-frame {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 23px;
  height: 23px;
  padding: 0;
  border: none;
  border-radius: 20px;
  background: rgba(0, 0, 0, 0.18);
  cursor: pointer;
  transition: background 0.15s ease;
}

.quote-pill__arrow-frame:hover {
  background: rgba(0, 0, 0, 0.28);
}

.quote-pill__arrow-frame::after {
  content: '';
  position: absolute;
  inset: 0;
  border: 1.5px solid rgba(255, 255, 255, 0.88);
  border-radius: 20px;
  pointer-events: none;
}

.quote-pill__arrow-icon {
  position: relative;
  z-index: 1;
  color: #fff;
}

.quote-pill__divider {
  flex-shrink: 0;
  width: 1px;
  height: 22px;
  margin-left: 3px;
  align-self: center;
  border-radius: 1px;
  background: rgba(255, 255, 255);
}

.quote-pill__text-slot {
  flex: 1;
  min-width: 0;
  height: 1.35em;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quote-pill__text {
  position: relative;
  width: 100%;
  margin: 0;
  font-family:
    'Noto Sans SC',
    'Manrope',
    'Noto Sans JP',
    system-ui,
    sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.35;
  text-align: center;
  letter-spacing: 0.02em;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quote-text-enter-active,
.quote-text-leave-active {
  transition:
    transform 0.48s cubic-bezier(0.33, 1, 0.68, 1),
    opacity 0.42s ease;
}

.quote-text-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.quote-text-enter-to {
  transform: translateY(0);
  opacity: 1;
}

.quote-text-leave-from {
  transform: translateY(0);
  opacity: 1;
}

.quote-text-leave-to {
  transform: translateY(-72%);
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .quote-text-enter-active,
  .quote-text-leave-active {
    transition: none;
  }

  .quote-text-enter-from,
  .quote-text-leave-to {
    transform: none;
    opacity: 1;
  }
}

@media (max-width: 640px) {
  .quote-pill {
    min-width: 0;
    max-width: min(94vw, 28ch);
  }

  .quote-pill__text {
    font-size: 11px;
  }
}
</style>
