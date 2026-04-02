import type { ErrorRequestHandler } from 'express'
import { ZodError } from 'zod'

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

  console.error(err)
  res.status(500).json({ error: 'internal_error' })
}
