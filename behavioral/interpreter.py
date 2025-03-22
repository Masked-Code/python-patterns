class Expression:
    def interpret(self, context): pass

class Number(Expression):
    def __init__(self, value): self.value = value
    def interpret(self, context): return self.value

class Add(Expression):
    def __init__(self, left, right): self.left = left; self.right = right
    def interpret(self, context): return self.left.interpret(context) + self.right.interpret(context)

expr = Add(Number(5), Number(3))
print(expr.interpret({}))  # 8