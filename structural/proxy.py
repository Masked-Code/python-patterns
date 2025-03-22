class Image:
    def display(self): pass

class RealImage(Image):
    def __init__(self, filename): self.filename = filename
    def display(self): return f"Displaying {self.filename}"

class ProxyImage(Image):
    def __init__(self, filename): self.filename = filename; self.image = None
    def display(self):
        if not self.image: self.image = RealImage(self.filename)
        return self.image.display()

img = ProxyImage("photo.jpg")
print(img.display())  # Displaying photo.jpg (loaded only once)