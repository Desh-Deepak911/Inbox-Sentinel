from inbox_sentinel.notifications.base import NotificationAdapter


class ConsoleNotificationAdapter(NotificationAdapter):
    def send(self, title, message, subtitle=None):
        print()
        print("=" * 80)
        print(title)

        if subtitle:
            print(f"From: {subtitle}")

        print(message)
        print("=" * 80)
        print()