class Handler:
    def __init__(self, successor=None): self.successor = successor
    def handle(self, request): pass

class Level1Support(Handler):
    def handle(self, request):
        if request <= 1: return "Level 1 handled"
        return self.successor.handle(request)

class Level2Support(Handler):
    def handle(self, request):
        if request <= 2: return "Level 2 handled"
        return self.successor.handle(request)

chain = Level1Support(Level2Support())
print(chain.handle(2))  # Level 2 handled