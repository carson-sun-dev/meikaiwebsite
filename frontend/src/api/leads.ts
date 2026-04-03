import type { ContactQuotePayload } from '@/components/contact/ContactQuoteForm.vue'

function apiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return base ? `${base}${p}` : p
}

async function readErrorMessage(res: Response): Promise<string> {
  const text = await res.text()
  if (!text.trim()) {
    if (res.status >= 500) return '服务暂时不可用，请稍后重试'
    if (res.status === 413) return '提交内容过大，请精简后重试'
    return `提交失败（${res.status}）`
  }
  try {
    const data = JSON.parse(text) as {
      error?: string
      message?: string
      messages?: Array<{ path?: string; message?: string }>
    }
    if (data.messages?.length) {
      return data.messages.map((m) => m.message).join('；')
    }
    if (typeof data.message === 'string' && data.message.trim()) {
      return data.message.trim()
    }
    if (data.error === 'validation_error') {
      return '请检查表单填写是否完整'
    }
    if (data.error === 'not_found') {
      return '接口不可用，请刷新页面后重试'
    }
    if (data.error) {
      return '提交失败，请稍后重试'
    }
  } catch {
    /* ignore */
  }
  return `提交失败（${res.status}）`
}

async function postJson<T>(url: string, body: unknown): Promise<T> {
  let res: Response
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch (e) {
    if (e instanceof TypeError) {
      throw new Error('网络连接失败，请检查网络后重试')
    }
    throw e
  }
  if (!res.ok) {
    throw new Error(await readErrorMessage(res))
  }
  return (await res.json()) as T
}

export async function submitQuoteLead(payload: ContactQuotePayload): Promise<{ id: number }> {
  const data = await postJson<{ ok: boolean; id: number }>(apiUrl('/api/leads/quote'), payload)
  return { id: data.id }
}

export async function submitFooterPhone(phone: string): Promise<{ id: number }> {
  const data = await postJson<{ ok: boolean; id: number }>(apiUrl('/api/leads/footer-phone'), {
    phone,
  })
  return { id: data.id }
}
