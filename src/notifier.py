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