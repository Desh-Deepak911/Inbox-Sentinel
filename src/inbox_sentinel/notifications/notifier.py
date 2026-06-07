from pync import Notifier


def notify_email(email):
    title = f"Inbox Sentinel: {email['priority']} priority"

    message = email.get("subject") or "New important email"

    sender = email.get("from", "Unknown sender")

    Notifier.notify(
        message,
        title=title,
        subtitle=sender,
        sound="default",
    )

def notify_reminder(reminder):
    title = f"Inbox Sentinel Reminder: {reminder['priority']}"

    message = reminder.get("suggested_action") or reminder.get("subject")

    sender = reminder.get("sender", "Unknown sender")

    Notifier.notify(
        message,
        title=title,
        subtitle=sender,
        sound="default",
    )