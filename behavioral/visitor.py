class Shape:
    def accept(self, visitor): pass

class Circle(Shape):
    def accept(self, visitor): return visitor.visit_circle(self)
    def radius(self): return 5

class Visitor:
    def visit_circle(self, circle): pass

class AreaVisitor(Visitor):
    def visit_circle(self, circle): return 3.14 * circle.radius() ** 2

circle = Circle()
visitor = AreaVisitor()
print(circle.accept(visitor))  # 78.5