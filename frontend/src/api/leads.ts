import type { ContactQuotePayload } from '@/components/contact/ContactQuoteForm.vue'

function apiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return base ? `${base}${p}` : p
}

async function readErrorMessage(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as {
      error?: string
      messages?: Array<{ path?: string; message?: string }>
    }
    if (data.messages?.length) {
      return data.messages.map((m) => m.message).join('；')
    }
    if (data.error === 'validation_error') {
      return '请检查表单填写是否完整'
    }
    if (data.error) {
      return '提交失败，请稍后重试'
    }
  } catch {
    /* ignore */
  }
  return `提交失败（${res.status}）`
}

export async function submitQuoteLead(payload: ContactQuotePayload): Promise<{ id: number }> {
  const res = await fetch(apiUrl('/api/leads/quote'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    throw new Error(await readErrorMessage(res))
  }
  const data = (await res.json()) as { ok: boolean; id: number }
  return { id: data.id }
}

export async function submitFooterPhone(phone: string): Promise<{ id: number }> {
  const res = await fetch(apiUrl('/api/leads/footer-phone'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone }),
  })
  if (!res.ok) {
    throw new Error(await readErrorMessage(res))
  }
  const data = (await res.json()) as { ok: boolean; id: number }
  return { id: data.id }
}
