class Coffee:
    def cost(self): return 5

class MilkDecorator:
    def __init__(self, coffee): self.coffee = coffee
    def cost(self): return self.coffee.cost() + 2

class SugarDecorator:
    def __init__(self, coffee): self.coffee = coffee
    def cost(self): return self.coffee.cost() + 1

coffee = Coffee()
coffee_with_milk = MilkDecorator(coffee)
coffee_with_sugar = SugarDecorator(coffee_with_milk)
print(coffee_with_sugar.cost())  # 8 (5 + 2 + 1)