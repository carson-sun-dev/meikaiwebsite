import mysql from 'mysql2/promise'

import { env } from '../config/env.js'
import { migrate } from './migrate.js'

export type Db = mysql.Pool

export async function createDatabase(): Promise<Db> {
  const pool = mysql.createPool({
    host: env.database.host,
    port: env.database.port,
    user: env.database.user,
    password: env.database.password,
    database: env.database.database,
    waitForConnections: true,
    // 2C/2G 等小规格机器上避免连接过多占用内存
    connectionLimit: env.nodeEnv === 'production' ? 5 : 10,
    maxIdle: env.nodeEnv === 'production' ? 3 : 5,
    idleTimeout: 60000,
    enableKeepAlive: true,
  })

  await migrate(pool)
  return pool
}
