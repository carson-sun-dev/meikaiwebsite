import type { Db } from './connection.js'

/** 留资内容在 payload_json（TEXT）中；表单选项增删改无需改表结构，与后端 quoteOptionKeys 对齐即可。 */
export async function migrate(pool: Db): Promise<void> {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS submissions (
      id INT AUTO_INCREMENT PRIMARY KEY,
      kind VARCHAR(32) NOT NULL,
      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      phone VARCHAR(32) NOT NULL,
      last_name VARCHAR(64) NULL,
      gender VARCHAR(16) NULL,
      plan_key VARCHAR(32) NULL,
      payload_json TEXT NOT NULL,
      CONSTRAINT chk_submissions_kind CHECK (kind IN ('quote', 'footer_phone')),
      KEY idx_submissions_created_at (created_at),
      KEY idx_submissions_kind (kind)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  `)
}
