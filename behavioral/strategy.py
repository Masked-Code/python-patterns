class SortStrategy:
    def sort(self, data): pass

class BubbleSort(SortStrategy):
    def sort(self, data): return sorted(data)  # Simplified

class QuickSort(SortStrategy):
    def sort(self, data): return sorted(data, reverse=True)  # Simplified

class Sorter:
    def __init__(self, strategy): self.strategy = strategy
    def sort(self, data): return self.strategy.sort(data)

sorter = Sorter(BubbleSort())
print(sorter.sort([3, 1, 2]))  # [1, 2, 3]