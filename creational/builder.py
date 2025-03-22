class Pizza:
    def __init__(self): self.toppings = []
    def __str__(self): return f"Pizza with {', '.join(self.toppings)}"

class PizzaBuilder:
    def __init__(self): self.pizza = Pizza()
    def add_cheese(self): self.pizza.toppings.append("cheese"); return self
    def add_pepperoni(self): self.pizza.toppings.append("pepperoni"); return self
    def build(self): return self.pizza

pizza = PizzaBuilder().add_cheese().add_pepperoni().build()
print(pizza)  # Pizza with cheese, pepperoni