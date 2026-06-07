from datetime import datetime, timedelta, timezone

from inbox_sentinel.memory.sqlite_store import get_connection


def cleanup_processed_emails(retention_days):
    deleted = 0

    with get_connection() as conn:
        for priority, days in retention_days.items():

            cutoff = (
                datetime.now(timezone.utc)
                - timedelta(days=days)
            ).isoformat()

            cursor = conn.execute(
                """
                DELETE FROM processed_emails
                WHERE priority = ?
                AND processed_at < ?
                """,
                (
                    priority,
                    cutoff,
                ),
            )

            deleted += cursor.rowcount

    return deleted

def cleanup_sent_reminders(retention_days):
    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(days=retention_days)
    ).isoformat()

    with get_connection() as conn:

        cursor = conn.execute(
            """
            DELETE FROM reminders
            WHERE status = 'sent'
            AND sent_at < ?
            """,
            (cutoff,),
        )

        return cursor.rowcount


def run_cleanup(config):
    if not config["cleanup"]["enabled"]:
        return

    email_deleted = cleanup_processed_emails(
        config["cleanup"]["retention_days"]
    )

    reminder_deleted = cleanup_sent_reminders(
        config["cleanup"]["reminder_retention_days"]
    )

    print(
        f"Cleanup complete. "
        f"Emails deleted={email_deleted}, "
        f"Reminders deleted={reminder_deleted}"
    )