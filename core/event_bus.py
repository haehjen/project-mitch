class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, callback):
        self.subscribers.setdefault(event_name, []).append(callback)

    def emit(self, event_name, data=None):
        for callback in self.subscribers.get(event_name, []):
            callback(data)