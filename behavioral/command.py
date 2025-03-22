class Light:
    def on(self): return "Light on"
    def off(self): return "Light off"

class Command:
    def execute(self): pass

class LightOnCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): return self.light.on()

light = Light()
command = LightOnCommand(light)
print(command.execute())  # Light on