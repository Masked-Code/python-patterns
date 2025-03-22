class CircuitBreaker:
    def __init__(self, failure_threshold=3):
        self.state = "CLOSED"
        self.failures = 0
        self.threshold = failure_threshold
    def call(self, func):
        if self.state == "OPEN": return "Circuit open, call blocked"
        try:
            result = func()
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold: self.state = "OPEN"
            return "Call failed"

def risky_call(): raise Exception("Oops")

cb = CircuitBreaker()
print(cb.call(risky_call))  # Call failed
print(cb.call(risky_call))  # Call failed
print(cb.call(risky_call))  # Circuit open, call blocked