import { createApp } from './app.js'
import { env } from './config/env.js'
import { createDatabase } from './db/connection.js'

try {
  const db = await createDatabase()
  const app = createApp(db)

  app.listen(env.port, () => {
    console.log(`[meikai-backend] listening on http://localhost:${env.port}`)
  })
} catch (err) {
  console.error('[meikai-backend] 启动失败（数据库或迁移）:', err)
  process.exit(1)
}
