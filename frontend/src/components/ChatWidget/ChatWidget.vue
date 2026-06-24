<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

import PhoneIcon from '@/components/icons/PhoneIcon.vue'
import logoImg from '@/source/logo/logo.webp'
import { useChatWidget } from '@/composables/useChatWidget'
import { scrollToSiteContact } from '@/composables/useScrollToSiteContact'

// 占位模式(2026-06-24 临时上线):AI 客服暂未开放,使用 ChatPanelPlaceholder。
// 恢复完整 AI 版本:把下一行 import 改回 './ChatPanel.vue' 即可,其他不动。
const ChatPanel = defineAsyncComponent(() => import('./ChatPanelPlaceholder.vue'))

const { isOpen, toggle, close } = useChatWidget()

function onContactClick() {
  close()
  scrollToSiteContact()
}
</script>

<template>
  <div class="chat-widget" :class="{ 'chat-widget--open': isOpen }">
    <ChatPanel v-if="isOpen" :compact-fab="isOpen" @close="close" />

    <div class="chat-widget__stack">
      <button
        v-show="!isOpen"
        type="button"
        class="chat-widget__fab chat-widget__fab--contact"
        aria-label="联系我们，跳转至页脚联系方式"
        @click="onContactClick"
      >
        <PhoneIcon class="chat-widget__contact-icon chat-widget__icon--desktop" />
        <span class="chat-widget__contact-text chat-widget__label--desktop">联系我们</span>
        <span class="chat-widget__grid-text chat-widget__label--mobile" aria-hidden="true">
          <span>联</span><span>系</span><span>我</span><span>们</span>
        </span>
      </button>

      <button
        type="button"
        class="chat-widget__fab chat-widget__fab--quote"
        :class="{ 'chat-widget__fab--open': isOpen }"
        :aria-label="isOpen ? '收起客服' : '打开 AI 客服 · 获取报价'"
        @click="toggle"
      >
        <template v-if="!isOpen">
          <span
            class="chat-widget__seal chat-widget__icon--desktop"
            :style="{ backgroundImage: `url(${logoImg})` }"
            aria-hidden="true"
          />
          <span class="chat-widget__text chat-widget__label--desktop">获取报价</span>
          <span class="chat-widget__grid-text chat-widget__label--mobile" aria-hidden="true">
            <span>获</span><span>取</span><span>报</span><span>价</span>
          </span>
        </template>
        <span v-else class="chat-widget__close" aria-hidden="true">×</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-widget {
  position: fixed;
  right: 24px;
  bottom: calc(40px + env(safe-area-inset-bottom, 0px));
  z-index: 10001;
  pointer-events: none;
}

.chat-widget__stack {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  pointer-events: auto;
}

.chat-widget__fab {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  outline: 0;
  cursor: pointer;
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  position: relative;
  transition:
    transform 0.4s cubic-bezier(0.2, 0.85, 0.3, 1.05),
    box-shadow 0.4s cubic-bezier(0.2, 0.85, 0.3, 1.05),
    background-color 0.3s ease,
    padding 0.3s ease;
}

.chat-widget__fab::after {
  content: '';
  position: absolute;
  inset: 4px;
  border-radius: inherit;
  border: 1px solid rgba(255, 255, 255, 0.22);
  pointer-events: none;
  transition: inset 0.4s cubic-bezier(0.2, 0.85, 0.3, 1.05);
}

.chat-widget__fab:hover {
  transform: translateY(-3px);
}

.chat-widget__fab:hover::after {
  inset: 6px;
}

/* 桌面：两钮等宽等高 */
@media (min-width: 768px) {
  .chat-widget__fab--contact,
  .chat-widget__fab--quote:not(.chat-widget__fab--open) {
    width: 124px;
    height: 44px;
    padding: 0 12px;
    gap: 7px;
    min-height: 44px;
    box-sizing: border-box;
    justify-content: center;
  }
}

/* —— 联系我们 —— */
.chat-widget__fab--contact {
  border-radius: 999px;
  background: #1a1a1a;
  color: #fff;
  box-shadow:
    0 6px 22px rgba(0, 0, 0, 0.28),
    0 0 0 1px rgba(255, 255, 255, 0.08);
}

.chat-widget__fab--contact:hover {
  background: #2a2a2a;
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.34),
    0 0 0 1px rgba(255, 255, 255, 0.12);
}

.chat-widget__fab--contact::after {
  border-color: rgba(255, 255, 255, 0.14);
}

.chat-widget__contact-icon {
  font-size: 16px;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  color: var(--mk-gold, #b8860b);
}

.chat-widget__contact-text {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.08em;
  line-height: 1;
  white-space: nowrap;
}

/* —— 获取报价 —— */
.chat-widget__fab--quote {
  border-radius: 999px;
  background: var(--mk-brand, #c41e3a);
  color: white;
  box-shadow:
    0 6px 22px rgba(196, 30, 58, 0.32),
    0 0 0 1px var(--mk-brand-dark, #8b1424);
}

.chat-widget__fab--quote:hover {
  background: var(--mk-brand-dark, #8b1424);
  box-shadow:
    0 12px 32px rgba(196, 30, 58, 0.42),
    0 0 0 1px var(--mk-brand-dark, #8b1424);
}

.chat-widget__seal {
  display: block;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: white;
  border-radius: 50%;
  padding: 2px;
  box-sizing: border-box;
}

.chat-widget__text {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.08em;
  line-height: 1;
  white-space: nowrap;
}

.chat-widget__fab--open {
  padding: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
}

.chat-widget__fab--open::after {
  inset: 5px;
  border-radius: 50%;
}

.chat-widget__close {
  font-size: 24px;
  line-height: 1;
  color: white;
  font-weight: 300;
}

/* 2×2 仅移动端；桌面默认隐藏(勿在 .grid-text 上写 display:grid,会盖掉 none) */
.chat-widget__label--mobile {
  display: none;
}

.chat-widget__grid-text {
  grid-template-columns: 1fr 1fr;
  gap: 1px 2px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: 0.02em;
  text-align: center;
}

@media (max-width: 767px) {
  .chat-widget {
    right: 16px;
    bottom: calc(32px + env(safe-area-inset-bottom, 0px));
  }

  /* 客服打开时圆钮置于面板之上,但不压住输入区(面板右侧已留空) */
  .chat-widget--open .chat-widget__stack {
    z-index: 10002;
  }

  .chat-widget__stack {
    gap: 8px;
  }

  .chat-widget__icon--desktop,
  .chat-widget__label--desktop {
    display: none !important;
  }

  .chat-widget__label--mobile {
    display: grid;
  }

  .chat-widget__fab--contact,
  .chat-widget__fab--quote {
    width: 58px;
    height: 58px;
    min-height: 58px;
    padding: 0;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .chat-widget__fab--open {
    width: 58px;
    height: 58px;
  }

  .chat-widget__fab--quote:not(.chat-widget__fab--open) {
    gap: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .chat-widget__fab {
    transition: none;
  }

  .chat-widget__fab:hover {
    transform: none;
  }
}
</style>
