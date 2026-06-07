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
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def is_email_processed(email_id):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT 1 FROM processed_emails WHERE id = ?",
            (email_id,),
        ).fetchone()

    return result is not None


def save_processed_email(email):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO processed_emails
            (id, thread_id, sender, subject, priority, score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                email["id"],
                email["thread_id"],
                email["from"],
                email["subject"],
                email["priority"],
                email["score"],
            ),
        )