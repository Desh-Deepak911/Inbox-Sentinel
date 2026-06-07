from abc import ABC, abstractmethod


class NotificationAdapter(ABC):
    @abstractmethod
    def send(self, title, message, subtitle=None):
        pass