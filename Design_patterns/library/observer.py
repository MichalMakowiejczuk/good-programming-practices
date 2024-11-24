class NotificationSystem:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, user):
        self.subscribers.append(user)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

class UserObserver:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"Notification for {self.name}: {message}")