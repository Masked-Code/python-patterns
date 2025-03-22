class Component:
    def operation(self): pass

class File(Component):
    def __init__(self, name): self.name = name
    def operation(self): return f"File: {self.name}"

class Directory(Component):
    def __init__(self, name): self.name = name; self.children = []
    def add(self, component): self.children.append(component)
    def operation(self): return f"Dir: {self.name}\n" + "\n".join(c.operation() for c in self.children)

dir1 = Directory("root")
dir1.add(File("file1.txt"))
dir1.add(File("file2.txt"))
print(dir1.operation())
# Dir: root
# File: file1.txt
# File: file2.txt