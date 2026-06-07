from pync import Notifier

from inbox_sentinel.notifications.base import NotificationAdapter


class MacNotificationAdapter(NotificationAdapter):
    def send(self, title, message, subtitle=None):
        Notifier.notify(
            message,
            title=title,
            subtitle=subtitle or "",
            sound="default",
        )