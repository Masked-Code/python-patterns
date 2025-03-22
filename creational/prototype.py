import copy

class Document:
    def __init__(self, content): self.content = content
    def clone(self): return copy.deepcopy(self)
    def __str__(self): return self.content

doc = Document("Original")
doc_copy = doc.clone()
print(doc_copy)  # Original