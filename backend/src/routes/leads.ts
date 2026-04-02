import type { Db } from '../db/connection.js'
import { createLeadsController } from '../controllers/leadsController.js'
import { Router } from 'express'

export function createLeadsRouter(db: Db) {
  const router = Router()
  const leads = createLeadsController(db)

  router.post('/quote', (req, res, next) => leads.postQuote(req, res, next))
  router.post('/footer-phone', (req, res, next) => leads.postFooterPhone(req, res, next))

  return router
}
