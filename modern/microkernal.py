class Editor:
    def __init__(self): self.plugins = {}
    def register_plugin(self, name, plugin): self.plugins[name] = plugin
    def execute(self, name): return self.plugins[name]() if name in self.plugins else "No plugin"

class SpellCheckPlugin:
    def __call__(self): return "Spell check done"

editor = Editor()
editor.register_plugin("spellcheck", SpellCheckPlugin())
print(editor.execute("spellcheck"))  # Spell check done