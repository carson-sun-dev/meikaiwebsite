import { createApp } from './app.js'
import { env } from './config/env.js'
import { createDatabase } from './db/connection.js'

const db = await createDatabase()
const app = createApp(db)

app.listen(env.port, () => {
  console.log(`[meikai-backend] listening on http://localhost:${env.port}`)
})
