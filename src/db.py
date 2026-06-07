import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "inbox_sentinel.sqlite3"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_emails (
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender TEXT,
                subject TEXT,
                priority TEXT,
                score INTEGER,
                ai_reason TEXT,
                suggested_action TEXT,
                confidence REAL,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        existing_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(processed_emails)")
        }

        migrations = {
            "ai_reason": "ALTER TABLE processed_emails ADD COLUMN ai_reason TEXT",
            "suggested_action": "ALTER TABLE processed_emails ADD COLUMN suggested_action TEXT",
            "confidence": "ALTER TABLE processed_emails ADD COLUMN confidence REAL",
        }

        for column, query in migrations.items():
            if column not in existing_columns:
                conn.execute(query)


def is_email_processed(email_id):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT 1 FROM processed_emails WHERE id = ?",
            (email_id,),
        ).fetchone()

    return result is not None

def get_recent_priority_emails(limit=20):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                sender,
                subject,
                priority,
                score,
                ai_reason,
                suggested_action,
                confidence,
                processed_at
            FROM processed_emails
            WHERE priority IN ('HIGH', 'MEDIUM')
            ORDER BY processed_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]

def save_processed_email(email):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO processed_emails
            (
                id,
                thread_id,
                sender,
                subject,
                priority,
                score,
                ai_reason,
                suggested_action,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email["id"],
                email["thread_id"],
                email["from"],
                email["subject"],
                email["priority"],
                email["score"],
                email.get("ai_reason"),
                email.get("suggested_action"),
                email.get("confidence"),
            ),
        )