class BookingSaga:
    def __init__(self): self.steps = []; self.compensations = []
    def add_step(self, action, compensation):
        self.steps.append(action); self.compensations.append(compensation)
    def execute(self):
        for i, step in enumerate(self.steps):
            try: step()
            except Exception:
                for comp in self.compensations[:i][::-1]: comp()
                return "Failed, rolled back"
        return "Success"

def book_flight(): print("Flight booked")
def cancel_flight(): print("Flight canceled")
saga = BookingSaga()
saga.add_step(book_flight, cancel_flight)
print(saga.execute())  # Flight booked\nSuccess