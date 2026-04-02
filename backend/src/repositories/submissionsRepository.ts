import type { ResultSetHeader } from 'mysql2'

import type { Db } from '../db/connection.js'
import type { QuotePayload } from '../validators/quoteSchema.js'

export type InsertQuoteResult = { id: number }

export async function insertQuoteLead(db: Db, payload: QuotePayload): Promise<InsertQuoteResult> {
  const [result] = await db.execute<ResultSetHeader>(
    `INSERT INTO submissions (kind, phone, last_name, gender, plan_key, payload_json)
     VALUES ('quote', ?, ?, ?, ?, ?)`,
    [
      payload.contact.phone.trim(),
      payload.contact.lastName.trim(),
      payload.contact.gender,
      payload.planKey,
      JSON.stringify(payload),
    ],
  )
  return { id: Number(result.insertId) }
}

export async function insertFooterPhoneLead(db: Db, phone: string): Promise<InsertQuoteResult> {
  const body = { source: 'footer', phone: phone.trim() }
  const [result] = await db.execute<ResultSetHeader>(
    `INSERT INTO submissions (kind, phone, last_name, gender, plan_key, payload_json)
     VALUES ('footer_phone', ?, NULL, NULL, NULL, ?)`,
    [phone.trim(), JSON.stringify(body)],
  )
  return { id: Number(result.insertId) }
}
