class Recipe:
    def cook(self): return f"{self.prepare()}\n{self.cook_main()}"
    def prepare(self): return "Preparing ingredients"
    def cook_main(self): pass

class Pasta(Recipe):
    def cook_main(self): return "Boiling pasta"

pasta = Pasta()
print(pasta.cook())
# Preparing ingredients
# Boiling pasta