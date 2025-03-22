class Button:
    def click(self): pass

class WinButton(Button):
    def click(self): return "Windows button clicked"

class MacButton(Button):
    def click(self): return "Mac button clicked"

class GUIFactory:
    def create_button(self): pass

class WinFactory(GUIFactory):
    def create_button(self): return WinButton()

class MacFactory(GUIFactory):
    def create_button(self): return MacButton()

factory = WinFactory()
button = factory.create_button()
print(button.click())  # Windows button clicked