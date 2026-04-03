import type { Db } from '../db/connection.js'
import { Router } from 'express'

import { healthRouter } from './health.js'
import { createLeadsRouter } from './leads.js'

export function createApiRouter(db: Db) {
  const api = Router()

  api.use(healthRouter)
  api.use('/leads', createLeadsRouter(db))
  api.use((_req, res) => {
    res.status(404).json({ error: 'not_found', message: '接口不存在' })
  })

  return api
}
