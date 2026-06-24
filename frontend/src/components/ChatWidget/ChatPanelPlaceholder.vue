<script setup lang="ts">
// 占位面板(2026-06-24 临时上线用):AI 客服后端仍在迭代,先用静态文案占位 + 禁用发送。
// 恢复方式:见同目录 ChatWidget.vue 顶部注释 — 一行 import 切回 ChatPanel.vue 即可。
// 注:外观与原 ChatPanel 保持一致,避免视觉抖动;不引入 aiChat / streamChat 任何调用。

defineProps<{
  /** 移动端:客服已打开时仅保留一个关闭圆钮,缩小底部留白 */
  compactFab?: boolean
}>()

defineEmits<{ close: [] }>()

const placeholderText =
  'AI 客服功能正在升级中,敬请期待。\n\n详情请致电:13393736352(微信同号)'
</script>

<template>
  <section
    class="chat-panel"
    :class="{ 'chat-panel--fab-compact': compactFab }"
    role="dialog"
    aria-label="美恺客服"
  >
    <header class="chat-panel__header">
      <div>
        <strong>美恺客服</strong>
        <span class="chat-panel__hint">AI 客服暂未开放<br>详情请致电:13393736352(微信同号)</span>
      </div>
      <button type="button" class="chat-panel__close" aria-label="关闭" @click="$emit('close')">
        ×
      </button>
    </header>

    <div class="chat-panel__body">
      <div class="chat-panel__msg chat-panel__msg--assistant">
        <div class="chat-panel__bubble">{{ placeholderText }}</div>
      </div>
    </div>

    <footer class="chat-panel__footer">
      <textarea
        rows="2"
        placeholder="AI 客服功能升级中,暂不可用"
        disabled
        aria-disabled="true"
      />
      <div class="chat-panel__actions">
        <button type="button" class="chat-panel__btn" disabled aria-disabled="true">
          发送
        </button>
      </div>
    </footer>
  </section>
</template>

<style scoped>
/* 样式与 ChatPanel.vue 严格对齐 — 后续切回时无需重排布局。
   差异仅在 textarea/btn 的 disabled 灰态。 */
.chat-panel {
  position: absolute;
  right: 0;
  bottom: 128px;
  width: 360px;
  max-width: calc(100vw - 28px);
  height: 520px;
  max-height: calc(100vh - 110px);
  max-height: calc(100dvh - 110px);
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.06);
  pointer-events: auto;
}

.chat-panel__header {
  flex-shrink: 0;
  padding: 12px 14px;
  background: var(--color-brand);
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-panel__hint {
  display: block;
  font-size: 11px;
  opacity: 0.85;
  margin-top: 2px;
}
.chat-panel__close {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 22px;
  cursor: pointer;
  line-height: 1;
  pointer-events: auto;
  position: relative;
  z-index: 2;
  padding: 6px 10px;
}
.chat-panel__close:hover {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
}
.chat-panel__close:active {
  background: rgba(255, 255, 255, 0.25);
}

.chat-panel__body {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  background: #f8f8f9;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-panel__msg {
  display: flex;
}
.chat-panel__msg--assistant {
  justify-content: flex-start;
}
.chat-panel__bubble {
  max-width: 78%;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
  background: #fff;
  color: #2b2b2b;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.chat-panel__footer {
  flex-shrink: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding: 8px 10px;
  background: #fff;
  position: relative;
  z-index: 2;
}
.chat-panel__footer textarea {
  width: 100%;
  resize: none;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
  background: #f3f3f5;
  color: #999;
  cursor: not-allowed;
}
.chat-panel__actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}
.chat-panel__btn {
  background: var(--color-brand);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 13px;
  min-height: 36px;
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 767px) {
  .chat-panel {
    --chat-fab-clearance: 168px;
    position: fixed;
    top: 76px;
    right: 12px;
    left: 12px;
    bottom: calc(var(--chat-fab-clearance) + env(safe-area-inset-bottom, 0px));
    width: auto;
    height: auto;
    max-width: none;
    max-height: none;
    border-radius: 14px;
    z-index: 10000;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.32);
  }

  .chat-panel--fab-compact {
    --chat-fab-clearance: 108px;
    right: 12px;
    left: 12px;
  }

  .chat-panel__header { padding: 12px 14px; }
  .chat-panel__header strong { font-size: 15px; }
  .chat-panel__hint { font-size: 11px; }
  .chat-panel__close {
    width: 36px; height: 36px;
    font-size: 24px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .chat-panel__body {
    padding: 12px;
    gap: 8px;
    min-height: 0;
    -webkit-overflow-scrolling: touch;
  }
  .chat-panel__bubble {
    font-size: 14.5px;
    padding: 9px 13px;
    max-width: 84%;
  }
  .chat-panel__footer {
    padding: 10px 12px calc(10px + env(safe-area-inset-bottom, 0px));
  }
  .chat-panel__footer textarea {
    font-size: 16px;
    min-height: 44px;
    line-height: 1.4;
  }
  .chat-panel__btn {
    padding: 8px 18px;
    font-size: 14px;
    min-height: 40px;
  }
}

@media (max-width: 380px) {
  .chat-panel {
    top: 70px;
    right: 8px;
    left: 8px;
    --chat-fab-clearance: 160px;
  }
  .chat-panel--fab-compact {
    --chat-fab-clearance: 102px;
  }
}
</style>
