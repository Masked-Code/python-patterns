class Color:
    def apply(self): pass

class Red(Color):
    def apply(self): return "Red"

class Blue(Color):
    def apply(self): return "Blue"

class Shape:
    def __init__(self, color): self.color = color
    def draw(self): pass

class Circle(Shape):
    def draw(self): return f"{self.color.apply()} Circle"

circle = Circle(Red())
print(circle.draw())  # Red Circle