class CPU:
    def start(self): return "CPU started"

class Memory:
    def load(self): return "Memory loaded"

class ComputerFacade:
    def __init__(self): self.cpu = CPU(); self.memory = Memory()
    def start(self): return f"{self.cpu.start()}\n{self.memory.load()}"

computer = ComputerFacade()
print(computer.start())
# CPU started
# Memory loaded