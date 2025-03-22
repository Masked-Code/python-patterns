class Logger:
    def log(self, message): return f"Logging: {message}"

class Service:
    def __init__(self, logger):  # Logger injected
        self.logger = logger
    def do_work(self):
        return self.logger.log("Work done")

logger = Logger()
service = Service(logger)  # Dependency injected
print(service.do_work())  # Logging: Work done