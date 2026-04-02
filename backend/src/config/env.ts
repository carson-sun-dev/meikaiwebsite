import path from 'node:path'
import { fileURLToPath } from 'node:url'

import dotenv from 'dotenv'

const __libdir = path.dirname(fileURLToPath(import.meta.url))

dotenv.config({ path: path.join(__libdir, '../../.env') })

function parseOrigins(raw: string | undefined): string[] {
  if (!raw?.trim()) {
    return ['http://localhost:5173', 'http://127.0.0.1:5173']
  }
  return raw
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

const port = Number(process.env.PORT) || 3001

export const env = {
  nodeEnv: process.env.NODE_ENV ?? 'development',
  port,
  database: {
    host: process.env.DATABASE_HOST?.trim() || '127.0.0.1',
    port: Number(process.env.DATABASE_PORT) || 3306,
    user: process.env.DATABASE_USER?.trim() || 'root',
    password: process.env.DATABASE_PASSWORD ?? '',
    database: process.env.DATABASE_NAME?.trim() || 'meikai',
  },
  corsOrigins: parseOrigins(process.env.CORS_ORIGINS),
} as const
