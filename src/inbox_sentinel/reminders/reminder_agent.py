from datetime import datetime, timedelta, timezone


PRIORITY_REMINDER_DELAYS = {
    "HIGH": timedelta(minutes=1),
    "MEDIUM": timedelta(minutes=2),
    "LOW": None,
}


def should_create_reminder(email):
    priority = email.get("priority")

    return priority in {"HIGH", "MEDIUM"}


def calculate_remind_at(priority):
    delay = PRIORITY_REMINDER_DELAYS.get(priority)

    if delay is None:
        return None

    return datetime.now(timezone.utc) + delay


def create_reminder(email):
    if not should_create_reminder(email):
        return None

    priority = email.get("priority")
    remind_at = calculate_remind_at(priority)

    if remind_at is None:
        return None

    return {
        "email_id": email.get("id"),
        "thread_id": email.get("thread_id"),
        "subject": email.get("subject"),
        "sender": email.get("from"),
        "priority": priority,
        "suggested_action": email.get("suggested_action"),
        "reason": email.get("ai_reason") or "; ".join(email.get("reasons", [])),
        "remind_at": remind_at.isoformat(),
        "status": "pending",
    }