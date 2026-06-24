/**
 * AI 客服跨组件状态总线 (2026-06-22)
 *
 * WHY module-level ref 而非 pinia / event bus:
 * - 只有"开 / 关 / 当前是否打开" 三个状态,不需要 store 完整生命周期
 * - 不引入新依赖;Vue 3 reactivity 跨组件天然工作(模块单例)
 * - 调用方语义:`const { open } = useChatWidget(); open()`,比 emit/listen 直观
 *
 * 入口点:
 * - ChatWidget.vue   订阅 isOpen + 提供 toggle 按钮
 * - HomeHeroSection  点 quote pill 触发 open() — 让"问报价"这个高频意图直接落到 AI
 * - 任意 CTA 按钮也可直接调 open() 替代 router.push('/contact')
 */
import { ref } from 'vue'

const isOpen = ref(false)

export function useChatWidget() {
  return {
    isOpen,
    open: () => { isOpen.value = true },
    close: () => { isOpen.value = false },
    toggle: () => { isOpen.value = !isOpen.value },
  }
}
