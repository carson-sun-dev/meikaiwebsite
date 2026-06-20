<script setup lang="ts">
import { ref } from 'vue'
import ChatPanel from './ChatPanel.vue'

const open = ref(false)

function toggle() {
  open.value = !open.value
}
</script>

<template>
  <div class="chat-widget">
    <ChatPanel v-if="open" @close="open = false" />
    <button
      type="button"
      class="chat-widget__fab"
      :class="{ 'chat-widget__fab--open': open }"
      :aria-label="open ? '关闭客服' : '打开 AI 客服'"
      @click="toggle"
    >
      <span v-if="!open" aria-hidden="true">💬</span>
      <span v-else aria-hidden="true">×</span>
    </button>
  </div>
</template>

<style scoped>
.chat-widget {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 9999;
}

.chat-widget__fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: var(--color-brand);
  color: #fff;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(196, 30, 58, 0.4);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.chat-widget__fab:hover {
  transform: scale(1.05);
}

.chat-widget__fab--open {
  font-size: 28px;
  line-height: 1;
}

@media (max-width: 767px) {
  .chat-widget {
    right: 14px;
    bottom: 14px;
  }
  .chat-widget__fab {
    width: 50px;
    height: 50px;
    font-size: 22px;
  }
}
</style>
