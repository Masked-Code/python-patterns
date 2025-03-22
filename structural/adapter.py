class OldSystem:
    def old_request(self): return "Old system data"

class NewSystem:
    def request(self): pass

class Adapter(NewSystem):
    def __init__(self, old): self.old = old
    def request(self): return self.old.old_request()

old = OldSystem()
adapter = Adapter(old)
print(adapter.request())  # Old system data