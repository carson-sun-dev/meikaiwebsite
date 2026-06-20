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
  | { type: 'delta'; text: string }
  | { type: 'done' }
  | { type: 'error'; code: string; msg: string }

export interface ChatStreamOptions {
  message: string
  signal?: AbortSignal
  onEvent: (e: AiSseEvent) => void
}

/**
 * 调用 /api/ai/chat 的 SSE 流。逐事件回调,调用方负责拼接 delta.text。
 * 协议见 ai-service/app/main.py:chat — event 字段是 delta|done|error,data 为 JSON。
 */
export async function streamChat(opts: ChatStreamOptions): Promise<void> {
  const { message, signal, onEvent } = opts
  const res = await fetch(apiUrl('/api/ai/chat'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
    body: JSON.stringify({ message }),
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
    buf += decoder.decode(value, { stream: true })

    // SSE 帧以空行分隔
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
