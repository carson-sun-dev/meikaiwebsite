import cors from 'cors'
import express from 'express'

import { env } from './config/env.js'
import type { Db } from './db/connection.js'
import { errorHandler } from './middleware/errorHandler.js'
import { createApiRouter } from './routes/index.js'

export function createApp(db: Db) {
  const app = express()

  // 经 Docker / Nginx 反代时正确解析客户端 IP（req.ip、日志等）
  if (env.nodeEnv === 'production') {
    app.set('trust proxy', 1)
  }

  app.use(
    cors({
      origin: env.corsOrigins,
      credentials: true,
    }),
  )
  app.use(express.json({ limit: '512kb' }))

  const api = createApiRouter(db)
  app.use('/api', api)

  app.use(errorHandler)
  return app
}
