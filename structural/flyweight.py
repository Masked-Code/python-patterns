class Character:
    def __init__(self, char): self.char = char
    def display(self, position): return f"{self.char} at {position}"

class CharacterFactory:
    def __init__(self): self.chars = {}
    def get_char(self, char):
        if char not in self.chars:
            self.chars[char] = Character(char)
        return self.chars[char]

factory = CharacterFactory()
c1 = factory.get_char("A")
c2 = factory.get_char("A")
print(c1.display(1))  # A at 1
print(c1 is c2)      # True (shared instance)