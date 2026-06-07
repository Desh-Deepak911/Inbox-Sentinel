from inbox_sentinel.notifications.console import ConsoleNotificationAdapter
from inbox_sentinel.notifications.mac import MacNotificationAdapter


def get_notification_adapter(channel="mac"):
    if channel == "console":
        return ConsoleNotificationAdapter()

    return MacNotificationAdapter()


def notify_email(email, channel="mac"):
    adapter = get_notification_adapter(channel)

    title = f"Inbox Sentinel: {email['priority']} priority"
    message = email.get("subject") or "New important email"
    subtitle = email.get("from", "Unknown sender")

    adapter.send(title, message, subtitle)


def notify_reminder(reminder, channel="mac"):
    adapter = get_notification_adapter(channel)

    title = f"Inbox Sentinel Reminder: {reminder['priority']}"
    message = reminder.get("suggested_action") or reminder.get("subject")
    subtitle = reminder.get("sender", "Unknown sender")

    adapter.send(title, message, subtitle)