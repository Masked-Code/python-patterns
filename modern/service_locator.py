class Logger:
    def log(self): return "Logged"

class ServiceLocator:
    def __init__(self): self.services = {}
    def register(self, name, service): self.services[name] = service
    def get(self, name): return self.services.get(name)

locator = ServiceLocator()
locator.register("logger", Logger())
logger = locator.get("logger")
print(logger.log())  # Logged