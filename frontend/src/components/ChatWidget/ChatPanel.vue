<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { streamChat, type AiSseEvent } from '@/api/aiChat'

const props = defineProps<{
  /** 移动端：客服已打开时仅保留一个关闭圆钮，缩小底部留白 */
  compactFab?: boolean
}>()

defineEmits<{ close: [] }>()

interface Message {
  role: 'user' | 'assistant'
  text: string
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    text: '您好👋，我是美恺客服～ \n今天有什么可以帮到您的？',
  },
  {
    role: 'assistant',
    text: '请告诉我您的需求～ \n您是想了解店铺装修？还是办公楼？还是家装？',
  },
])

const input = ref('')
const streaming = ref(false)
const errorMsg = ref('')
const scrollerRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)
const keyboardInset = ref(0)
// 首轮空,服务端 meta 回的 conversation_id 在这里保存,后续轮回带,thread_id 不变 → 跨轮 state 持久化
const conversationId = ref<string | null>(null)

let abortCtl: AbortController | null = null

/** 渲染前剥离 <quote_block> 标签 — LLM 按 prompt 把整段合规模板包在标签里,
 * 标签本身仅供 Guardrail 定位用,用户不该看到。流式 token 拼起来的 text 也可能含半截标签,
 * 用 g/i 全局正则一次性清掉<quote_block> / </quote_block>. */
function cleanBubble(text: string): string {
  return text.replace(/<\/?quote_block>/gi, '').replace(/\n{3,}/g, '\n\n').trim()
}

/** 把缓冲文本按 \n\n 切段后,用 1-3s 浮动延时 + typing dots 占位逐段 push 新气泡(真人打字感) */
function queueSegments(buffer: string) {
  const segments = cleanBubble(buffer).split(/\n{2,}/).map(s => s.trim()).filter(Boolean)
  if (segments.length === 0) return
  let accumDelay = 0
  for (const seg of segments) {
    const gap = 1000 + Math.random() * 2000   // 1-3s 浮动
    accumDelay += gap
    setTimeout(() => {
      // 1. 先 push 空气泡触发 typing dots 动画
      messages.value.push({ role: 'assistant', text: '' })
      const newIdx = messages.value.length - 1
      scrollToBottom()
      // 2. 短暂"思考"后填入内容(模拟 AI 开始回复)
      setTimeout(() => {
        if (messages.value[newIdx]) messages.value[newIdx].text = seg
        scrollToBottom()
      }, 500)
    }, accumDelay)
  }
}

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

  // 实时分段状态:第一段流式吐字 → 遇 \n\n 立即固定 → 后续 chunk 累积到 tailBuffer
  // 这样不会出现"先全显示再裁剪"的视觉跳变(用户截图反馈 2026-06-23)
  let firstSegmentDone = false
  let tailBuffer = ''

  try {
    await streamChat({
      message: text,
      conversationId: conversationId.value,
      signal: abortCtl.signal,
      onEvent: (e: AiSseEvent) => {
        if (e.type === 'meta') {
          if (e.conversationId && !conversationId.value) conversationId.value = e.conversationId
          return
        }
        if (e.type === 'error') {
          errorMsg.value = e.msg
          return
        }
        if (e.type !== 'delta') return

        // 第一段已切完 → chunk 直接进尾部 buffer,不再追加当前气泡
        if (firstSegmentDone) {
          tailBuffer += e.text
          return
        }

        const target = messages.value[idx]
        if (!target) return
        target.text += e.text

        // 实时检测段落分界,出现 \n\n 立即切段
        const cleaned = cleanBubble(target.text)
        const splitIdx = cleaned.indexOf('\n\n')
        if (splitIdx > 0) {
          target.text = cleaned.slice(0, splitIdx).trim()
          tailBuffer = cleaned.slice(splitIdx + 2)   // 剩余进尾部 buffer
          firstSegmentDone = true
        }
        scrollToBottom()
      },
    })
    // 流式结束 → 尾部 buffer 按 \n\n 切,1-3s 浮动延时 + dots 占位逐段推送
    if (tailBuffer.trim()) {
      queueSegments(tailBuffer)
    }
  } catch (e) {
    if ((e as Error).name === 'AbortError') return
    errorMsg.value = (e as Error).message || '很抱歉，貌似出现了错误。详情请致电：13393736352（微信同号）'
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

function updateKeyboardInset() {
  if (typeof window === 'undefined' || window.innerWidth > 767) {
    keyboardInset.value = 0
    return
  }
  const vv = window.visualViewport
  if (!vv) {
    keyboardInset.value = 0
    return
  }
  keyboardInset.value = Math.max(0, Math.round(window.innerHeight - vv.height - vv.offsetTop))
}

function onInputFocus() {
  updateKeyboardInset()
  // 等软键盘动画后再把输入区滚进可视范围
  window.setTimeout(() => {
    inputRef.value?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
    scrollToBottom()
  }, 280)
}

onMounted(() => {
  updateKeyboardInset()
  window.visualViewport?.addEventListener('resize', updateKeyboardInset)
  window.visualViewport?.addEventListener('scroll', updateKeyboardInset)
})

onUnmounted(() => {
  window.visualViewport?.removeEventListener('resize', updateKeyboardInset)
  window.visualViewport?.removeEventListener('scroll', updateKeyboardInset)
})
</script>

<template>
  <section
    class="chat-panel"
    :class="{ 'chat-panel--fab-compact': props.compactFab }"
    :style="keyboardInset > 0 ? { '--chat-keyboard-inset': `${keyboardInset}px` } : undefined"
    role="dialog"
    aria-label="AI 客服"
  >
    <header class="chat-panel__header">
      <div>
        <strong>美恺客服</strong>
        <span class="chat-panel__hint">AI 聊天内容可能有误<br> 会话仅供参考 · 详情请致电：13393736352（微信同号）</span>
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
        <!-- 纯文本渲染:避免 LLM 注入 HTML;cleanBubble 实时剥 <quote_block> 标签 -->
        <div class="chat-panel__bubble">
          <template v-if="m.text">{{ cleanBubble(m.text) }}</template>
          <span
            v-else-if="streaming && i === messages.length - 1"
            class="chat-panel__typing"
            aria-label="AI 正在输入"
          >
            <span></span><span></span><span></span>
          </span>
        </div>
      </div>
      <p v-if="errorMsg" class="chat-panel__err">{{ errorMsg }}</p>
    </div>

    <footer class="chat-panel__footer">
      <textarea
        ref="inputRef"
        v-model="input"
        rows="2"
        enterkeyhint="send"
        autocomplete="off"
        autocapitalize="sentences"
        :placeholder="streaming ? 'AI 正在回复…' : '请描述您的需求'"
        :disabled="streaming"
        @keydown="handleKey"
        @focus="onInputFocus"
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
  /* 显式声明可点 + 高于内层 — 防止被某些 stacking context 误覆盖 */
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

/* 跳点动画:替代 "..." 静态字符,模拟真人正在输入感觉 */
.chat-panel__typing {
  display: inline-flex;
  gap: 5px;
  align-items: center;
  padding: 4px 2px;
}
.chat-panel__typing span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  animation: chat-typing-bounce 1.2s ease-in-out infinite;
}
.chat-panel__typing span:nth-child(2) { animation-delay: 0.18s; }
.chat-panel__typing span:nth-child(3) { animation-delay: 0.36s; }
@keyframes chat-typing-bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
  .chat-panel__typing span { animation: none; opacity: 0.7; }
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
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
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
  padding: 8px 18px;
  font-size: 13px;
  cursor: pointer;
  min-height: 36px;
  touch-action: manipulation;
}
.chat-panel__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.chat-panel__btn--ghost {
  background: #eee;
  color: #444;
}

/* 移动端: top+bottom 双向定位,避免超出视口;底部为固定圆钮留空 */
@media (max-width: 767px) {
  .chat-panel {
    --chat-fab-clearance: 168px;
    --chat-keyboard-inset: 0px;
    position: fixed;
    top: 76px;
    right: 12px;
    left: 12px;
    bottom: calc(var(--chat-fab-clearance) + var(--chat-keyboard-inset) + env(safe-area-inset-bottom, 0px));
    width: auto;
    height: auto;
    max-width: none;
    max-height: none;
    border-radius: 14px;
    z-index: 10000;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.32);
  }

  /* 客服打开时仅余一个关闭圆钮,缩小底部留白避免输入区被挡 */
  .chat-panel--fab-compact {
    --chat-fab-clearance: 108px;
    right: 12px;
    left: 12px;
  }
  /* 不再给 footer 留 fab 右侧列 — fab 实际在 panel 外侧下方(bottom 24px 离 panel 144px),
     不重叠;之前 padding-right: 76px 导致右侧大段留白(用户反馈) */

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
    font-size: 16px; /* iOS 防 focus 时自动放大 */
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
  }

  .chat-panel:not(.chat-panel--fab-compact) {
    --chat-fab-clearance: 160px;
  }

  .chat-panel--fab-compact {
    --chat-fab-clearance: 102px;
  }
}
</style>
