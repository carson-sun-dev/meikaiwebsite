import type { Db } from './connection.js'

/**
 * Schema 演进规则:幂等(`CREATE TABLE IF NOT EXISTS`),只增不删;
 * 旧表 `submissions` 维持现状,AI 服务转人工时通过 backend /api/leads 写入。
 */
export async function migrate(pool: Db): Promise<void> {
  // 留资:与表单选项解耦,改字段无需改表结构(payload_json 承载)
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

  // AI 会话主表:visitor_fp 来自前端 ai_sid cookie(SameSite=Strict),30 天 TTL
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ai_sessions (
      session_id    CHAR(32) NOT NULL PRIMARY KEY,
      visitor_fp    VARCHAR(64) NULL,
      business_line VARCHAR(16) NULL,
      created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      KEY idx_ai_sessions_visitor (visitor_fp, updated_at),
      KEY idx_ai_sessions_updated (updated_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  `)

  // LangGraph checkpoint:用 langgraph-checkpoint-mysql 社区包(DESIGN §13.1);
  // 字段名对齐其 schema,后续可直接 wire saver
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ai_checkpoints (
      session_id  CHAR(32) NOT NULL,
      thread_ts   BIGINT   NOT NULL,
      parent_ts   BIGINT   NULL,
      state_json  MEDIUMTEXT NOT NULL,
      created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (session_id, thread_ts),
      KEY idx_ai_checkpoints_session (session_id, created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  `)

  // 数据飞轮:前端 👍/👎(DESIGN §11.2),trace_id 关联 LangFuse
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ai_feedback (
      id          BIGINT AUTO_INCREMENT PRIMARY KEY,
      session_id  CHAR(32) NOT NULL,
      trace_id    VARCHAR(64) NULL,
      score       TINYINT NOT NULL,
      comment     TEXT NULL,
      created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      CONSTRAINT chk_ai_feedback_score CHECK (score IN (-1, 1)),
      KEY idx_ai_feedback_session (session_id),
      KEY idx_ai_feedback_created (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  `)
}
