class MessageBroker:
    def __init__(self): self.subscribers = {}
    def subscribe(self, topic, subscriber): 
        self.subscribers.setdefault(topic, []).append(subscriber)
    def publish(self, topic, message):
        for sub in self.subscribers.get(topic, []): sub(message)

class Subscriber:
    def __init__(self, name): self.name = name
    def __call__(self, message): print(f"{self.name} received: {message}")

broker = MessageBroker()
sub1 = Subscriber("Sub1")
broker.subscribe("news", sub1)
broker.publish("news", "Breaking!")  # Sub1 received: Breaking!