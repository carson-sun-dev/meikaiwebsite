<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { streamChat, type AiSseEvent } from '@/api/aiChat'

defineEmits<{ close: [] }>()

interface Message {
  role: 'user' | 'assistant'
  text: string
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    text: '您好,我是美恺装饰的 AI 客服。可以告诉我您的装修需求,我帮您给一个参考区间;精确报价请联系我们的人工。',
  },
])

const input = ref('')
const streaming = ref(false)
const errorMsg = ref('')
const scrollerRef = ref<HTMLElement | null>(null)
// 首轮空,服务端 meta 回的 conversation_id 在这里保存,后续轮回带,thread_id 不变 → 跨轮 state 持久化
const conversationId = ref<string | null>(null)

let abortCtl: AbortController | null = null

async function send() {
  const text = input.value.trim()
  if (!text || streaming.value) return

  input.value = ''
  errorMsg.value = ''
  messages.value.push({ role: 'user', text })
  messages.value.push({ role: 'assistant', text: '' })
  await scrollToBottom()

  streaming.value = true
  abortCtl = new AbortController()
  const idx = messages.value.length - 1

  try {
    await streamChat({
      message: text,
      conversationId: conversationId.value,
      signal: abortCtl.signal,
      onEvent: (e: AiSseEvent) => {
        const target = messages.value[idx]
        if (e.type === 'meta') {
          if (e.conversationId && !conversationId.value) conversationId.value = e.conversationId
        } else if (e.type === 'delta' && target) {
          target.text += e.text
          scrollToBottom()
        } else if (e.type === 'error') {
          errorMsg.value = e.msg
        }
        // 'done' 不需要处理,流自然结束
      },
    })
  } catch (e) {
    if ((e as Error).name === 'AbortError') return
    errorMsg.value = (e as Error).message || '网络错误,请稍后重试'
  } finally {
    streaming.value = false
    abortCtl = null
  }
}

function cancel() {
  abortCtl?.abort()
}

async function scrollToBottom() {
  await nextTick()
  const el = scrollerRef.value
  if (el) el.scrollTop = el.scrollHeight
}

function handleKey(e: KeyboardEvent) {
  // Enter 发送,Shift+Enter 换行
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <section class="chat-panel" role="dialog" aria-label="AI 客服">
    <header class="chat-panel__header">
      <div>
        <strong>美恺 AI 客服</strong>
        <span class="chat-panel__hint">参考报价 · 精确请联系人工</span>
      </div>
      <button type="button" class="chat-panel__close" aria-label="关闭" @click="$emit('close')">
        ×
      </button>
    </header>

    <div ref="scrollerRef" class="chat-panel__body">
      <div
        v-for="(m, i) in messages"
        :key="i"
        class="chat-panel__msg"
        :class="m.role === 'user' ? 'chat-panel__msg--user' : 'chat-panel__msg--assistant'"
      >
        <!-- 纯文本渲染:避免 LLM 注入 HTML。Markdown 渲染待装 markdown-it + DOMPurify 后再开 -->
        <div class="chat-panel__bubble">{{ m.text || (streaming && i === messages.length - 1 ? '...' : '') }}</div>
      </div>
      <p v-if="errorMsg" class="chat-panel__err">{{ errorMsg }}</p>
    </div>

    <footer class="chat-panel__footer">
      <textarea
        v-model="input"
        rows="2"
        :placeholder="streaming ? 'AI 正在回复…' : '描述您的需求,Enter 发送'"
        :disabled="streaming"
        @keydown="handleKey"
      />
      <div class="chat-panel__actions">
        <button v-if="streaming" type="button" class="chat-panel__btn chat-panel__btn--ghost" @click="cancel">
          停止
        </button>
        <button
          v-else
          type="button"
          class="chat-panel__btn"
          :disabled="!input.trim()"
          @click="send"
        >
          发送
        </button>
      </div>
    </footer>
  </section>
</template>

<style scoped>
.chat-panel {
  position: absolute;
  right: 0;
  bottom: 72px;
  width: 360px;
  max-width: calc(100vw - 28px);
  height: 520px;
  max-height: calc(100vh - 110px);
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.chat-panel__header {
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
.chat-panel__msg--user {
  justify-content: flex-end;
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
}
.chat-panel__msg--user .chat-panel__bubble {
  background: var(--color-brand);
  color: #fff;
}
.chat-panel__msg--assistant .chat-panel__bubble {
  background: #fff;
  color: #2b2b2b;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.chat-panel__err {
  font-size: 12px;
  color: #c41e3a;
  margin: 4px 0 0;
}

.chat-panel__footer {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding: 8px 10px;
  background: #fff;
}
.chat-panel__footer textarea {
  width: 100%;
  resize: none;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}
.chat-panel__footer textarea:focus {
  border-color: var(--color-brand);
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
  padding: 6px 16px;
  font-size: 13px;
  cursor: pointer;
}
.chat-panel__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.chat-panel__btn--ghost {
  background: #eee;
  color: #444;
}

@media (max-width: 767px) {
  .chat-panel {
    right: 0;
    bottom: 64px;
    width: calc(100vw - 28px);
    height: calc(100vh - 100px);
  }
}
</style>
