/**
 * AI 客服 SSE 客户端(DESIGN §9.2.5)。
 *
 * 为什么 fetch + ReadableStream 而不是 EventSource:
 * - EventSource 不能 POST、不能带 body、不能带自定义 header
 * - 此处需要 POST JSON + Cookie(SameSite=Strict ai_sid)
 */

function apiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return base ? `${base}${p}` : p
}

export type AiSseEvent =
  | { type: 'meta'; conversationId?: string; businessLine?: string }
  | { type: 'delta'; text: string }
  | { type: 'done' }
  | { type: 'error'; code: string; msg: string }

export interface ChatStreamOptions {
  message: string
  // WHY 必传 conversationId:ai-service 用它做 thread_id,跨轮持久化 router/slots state;
  // 不传则每轮新生成,checkpointer 跨轮接续失效(Sprint 2 step 6 槽位多轮记忆白做)
  conversationId?: string | null
  signal?: AbortSignal
  onEvent: (e: AiSseEvent) => void
}

/**
 * 调用 /api/ai/chat 的 SSE 流。逐事件回调,调用方负责拼接 delta.text。
 * 协议见 ai-service/app/main.py:chat — event 字段是 meta|delta|done|error,data 为 JSON。
 */
export async function streamChat(opts: ChatStreamOptions): Promise<void> {
  const { message, conversationId, signal, onEvent } = opts
  const body: Record<string, unknown> = { message }
  if (conversationId) body.conversation_id = conversationId

  const res = await fetch(apiUrl('/api/ai/chat'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
    body: JSON.stringify(body),
    credentials: 'include',
    signal,
  })

  if (!res.ok || !res.body) {
    const text = res.ok ? '响应体为空' : await res.text().catch(() => '')
    throw new Error(text || `请求失败(${res.status})`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buf = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    // WHY \r\n → \n 归一化:sse_starlette 默认按 SSE 标准用 CRLF 行结束(字节级是
    // 0d0a0d0a 分帧),前端如果只 indexOf('\n\n') 等价于找 0a0a 子串,在 0d0a0d0a
    // 中找不到 → 永远 detect 不到帧结束 → onEvent 永不触发 → 气泡永远空白。
    // 实测复现:浏览器 fetch 收到的 buf 就是 0d0a0d0a。归一后用 \n\n 分帧就对了。
    buf += decoder.decode(value, { stream: true }).replace(/\r\n/g, '\n')

    let idx = buf.indexOf('\n\n')
    while (idx >= 0) {
      const frame = buf.slice(0, idx)
      buf = buf.slice(idx + 2)
      const ev = parseFrame(frame)
      if (ev) onEvent(ev)
      idx = buf.indexOf('\n\n')
    }
  }
}

function parseFrame(frame: string): AiSseEvent | null {
  let event = 'message'
  const dataLines: string[] = []
  for (const line of frame.split('\n')) {
    if (line.startsWith('event:')) event = line.slice(6).trim()
    else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim())
  }
  if (!dataLines.length) return null
  const data = dataLines.join('\n')

  try {
    const obj = JSON.parse(data) as Record<string, unknown>
    if (event === 'meta') {
      return {
        type: 'meta',
        conversationId: typeof obj.conversation_id === 'string' ? obj.conversation_id : undefined,
        businessLine: typeof obj.business_line === 'string' ? obj.business_line : undefined,
      }
    }
    if (event === 'delta' && typeof obj.text === 'string') {
      return { type: 'delta', text: obj.text }
    }
    if (event === 'done') return { type: 'done' }
    if (event === 'error') {
      return {
        type: 'error',
        code: String(obj.code ?? 'unknown'),
        msg: String(obj.msg ?? '未知错误'),
      }
    }
  } catch {
    // 忽略畸形帧
  }
  return null
}
