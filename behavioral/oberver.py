class NewsAgency:
    def __init__(self): self.subscribers = []; self.news = ""
    def subscribe(self, sub): self.subscribers.append(sub)
    def notify(self): return [sub.update(self.news) for sub in self.subscribers]
    def add_news(self, news): self.news = news; self.notify()

class Subscriber:
    def update(self, news): return f"Got news: {news}"

agency = NewsAgency()
sub = Subscriber()
agency.subscribe(sub)
agency.add_news("Breaking!")  # [Got news: Breaking!]