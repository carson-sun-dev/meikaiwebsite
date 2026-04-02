import type { Request, Response } from 'express'

import type { Db } from '../db/connection.js'
import { asyncHandler } from '../middleware/asyncHandler.js'
import { insertFooterPhoneLead, insertQuoteLead } from '../repositories/submissionsRepository.js'
import { footerPhoneBodySchema } from '../validators/footerPhoneSchema.js'
import { quotePayloadSchema } from '../validators/quoteSchema.js'

export function createLeadsController(db: Db) {
  return {
    postQuote: asyncHandler(async (req: Request, res: Response) => {
      const payload = quotePayloadSchema.parse(req.body)
      const { id } = await insertQuoteLead(db, payload)
      res.status(201).json({ ok: true, id })
    }),

    postFooterPhone: asyncHandler(async (req: Request, res: Response) => {
      const { phone } = footerPhoneBodySchema.parse(req.body)
      const { id } = await insertFooterPhoneLead(db, phone)
      res.status(201).json({ ok: true, id })
    }),
  }
}
