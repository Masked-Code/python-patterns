class MyList:
    def __init__(self, items): self.items = items; self.index = 0
    def __iter__(self): return self
    def __next__(self):
        if self.index < len(self.items):
            result = self.items[self.index]
            self.index += 1
            return result
        raise StopIteration

lst = MyList([1, 2, 3])
for item in lst: print(item)  # 1 2 3