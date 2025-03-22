class Memento:
    def __init__(self, state): self.state = state

class Editor:
    def __init__(self): self.content = ""
    def write(self, text): self.content += text
    def save(self): return Memento(self.content)
    def restore(self, memento): self.content = memento.state

editor = Editor()
editor.write("Hello")
memento = editor.save()
editor.write(" World")
editor.restore(memento)
print(editor.content)  # Hello