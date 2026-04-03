import type { ErrorRequestHandler } from 'express'
import { ZodError } from 'zod'

type ErrLike = {
  type?: string
  status?: number
  statusCode?: number
  code?: string
}

function getErrCode(err: unknown): string | undefined {
  if (typeof err !== 'object' || err === null || !('code' in err)) return undefined
  const c = (err as { code: unknown }).code
  return typeof c === 'string' ? c : undefined
}

export const errorHandler: ErrorRequestHandler = (err, _req, res, next) => {
  if (res.headersSent) {
    next(err)
    return
  }

  if (err instanceof ZodError) {
    const messages = err.issues.map((e) => ({
      path: e.path.join('.'),
      message: e.message,
    }))
    res.status(400).json({
      error: 'validation_error',
      messages,
    })
    return
  }

  const e = err as ErrLike

  if (e.type === 'entity.parse.failed') {
    res.status(400).json({
      error: 'invalid_json',
      message: '请求体格式不正确',
    })
    return
  }

  if (e.type === 'entity.too.large') {
    res.status(413).json({
      error: 'payload_too_large',
      message: '请求内容过大',
    })
    return
  }

  const errCode = getErrCode(err)
  if (errCode) {
    const transient = new Set([
      'ECONNREFUSED',
      'ETIMEDOUT',
      'PROTOCOL_CONNECTION_LOST',
      'PROTOCOL_ENQUEUE_AFTER_QUIT',
    ])
    if (transient.has(errCode)) {
      console.error('[mysql]', err)
      res.status(503).json({
        error: 'service_unavailable',
        message: '服务暂时不可用，请稍后重试',
      })
      return
    }
    if (errCode.startsWith('ER_')) {
      console.error('[mysql]', err)
      res.status(500).json({
        error: 'database_error',
        message: '保存失败，请稍后重试',
      })
      return
    }
  }

  const status = e.status ?? e.statusCode
  if (status === 400 && err instanceof SyntaxError) {
    res.status(400).json({
      error: 'invalid_json',
      message: '请求体格式不正确',
    })
    return
  }

  console.error(err)
  res.status(500).json({
    error: 'internal_error',
    message: '服务器异常，请稍后重试',
  })
}
