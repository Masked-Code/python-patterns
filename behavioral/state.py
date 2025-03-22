class State:
    def handle(self): pass

class Green(State):
    def handle(self): return "Green: Go"

class Red(State):
    def handle(self): return "Red: Stop"

class TrafficLight:
    def __init__(self): self.state = Green()
    def change(self): self.state = Red() if isinstance(self.state, Green) else Green()
    def signal(self): return self.state.handle()

light = TrafficLight()
print(light.signal())  # Green: Go
light.change()
print(light.signal())  # Red: Stop