from abc import ABC, abstractmethod
import threading
from typing import List, Dict
import time

# Creational Pattern: Builder
# Constructs complex Document objects step-by-step
class Document:
    def __init__(self):
        self.title = ""
        self.content = []
        self.format = "plain"

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nFormat: {self.format}"

class DocumentBuilder:
    def __init__(self):
        self.document = Document()

    def set_title(self, title: str) -> 'DocumentBuilder':
        self.document.title = title
        return self

    def add_content(self, content: str) -> 'DocumentBuilder':
        self.document.content.append(content)
        return self

    def set_format(self, format: str) -> 'DocumentBuilder':
        self.document.format = format
        return self

    def build(self) -> Document:
        return self.document

# Structural Pattern: Composite
# Treats individual elements and groups uniformly (e.g., text and sections)
class DocumentComponent(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class TextElement(DocumentComponent):
    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return self.text

class Section(DocumentComponent):
    def __init__(self, title: str):
        self.title = title
        self.components: List[DocumentComponent] = []

    def add(self, component: DocumentComponent):
        self.components.append(component)

    def render(self) -> str:
        result = f"Section: {self.title}\n"
        for component in self.components:
            result += f"  {component.render()}\n"
        return result

# Structural Pattern: Proxy
# Controls access to document rendering (e.g., lazy loading or access control)
class DocumentRenderer:
    def render(self, doc: Document) -> str:
        return f"Rendering {doc.title} in {doc.format}: {''.join(doc.content)}"

class DocumentRendererProxy:
    def __init__(self):
        self.renderer = None
        self.cache = None

    def render(self, doc: Document) -> str:
        if self.renderer is None:
            self.renderer = DocumentRenderer()  # Lazy initialization
        if self.cache != doc:
            self.cache = doc
            return self.renderer.render(doc)
        return "Cached render"

# Behavioral Pattern: Command
# Encapsulates editing actions as objects for undo/redo
class EditCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddTextCommand(EditCommand):
    def __init__(self, doc: Document, text: str):
        self.doc = doc
        self.text = text

    def execute(self):
        self.doc.content.append(self.text)

    def undo(self):
        self.doc.content.pop()

class Editor:
    def __init__(self):
        self.history: List[EditCommand] = []

    def execute_command(self, command: EditCommand):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()

# Behavioral Pattern: State
# Manages document states (e.g., Draft, Published)
class DocumentState(ABC):
    @abstractmethod
    def edit(self, doc: Document, editor: Editor, text: str):
        pass

    @abstractmethod
    def publish(self, doc: Document) -> str:
        pass

class DraftState(DocumentState):
    def edit(self, doc: Document, editor: Editor, text: str):
        editor.execute_command(AddTextCommand(doc, text))
        return "Text added in draft"

    def publish(self, doc: Document) -> str:
        doc.format = "published"
        return "Document published"

class PublishedState(DocumentState):
    def edit(self, doc: Document, editor: Editor, text: str):
        return "Cannot edit published document"

    def publish(self, doc: Document) -> str:
        return "Already published"

class DocumentContext:
    def __init__(self):
        self.state = DraftState()
        self.doc = Document()

    def set_state(self, state: DocumentState):
        self.state = state

    def edit(self, editor: Editor, text: str):
        return self.state.edit(self.doc, editor, text)

    def publish(self) -> str:
        result = self.state.publish(self.doc)
        if "published" in result.lower():
            self.set_state(PublishedState())
        return result

# Modern Pattern: Event Sourcing
# Tracks document changes as a sequence of events
class DocumentEvent:
    def __init__(self, event_type: str, data: Dict):
        self.event_type = event_type
        self.data = data

class EventStore:
    def __init__(self):
        self.events: List[DocumentEvent] = []

    def add_event(self, event: DocumentEvent):
        self.events.append(event)

    def replay(self, doc: Document):
        for event in self.events:
            if event.event_type == "add_text":
                doc.content.append(event.data["text"])

# Main execution
if __name__ == "__main__":
    # Builder to create a document
    builder = DocumentBuilder()
    doc = builder.set_title("My Doc").add_content("Intro").set_format("draft").build()

    # Composite for document structure
    section = Section("Chapter 1")
    section.add(TextElement("Paragraph 1"))
    section.add(TextElement("Paragraph 2"))
    print(section.render())

    # Proxy for rendering
    proxy = DocumentRendererProxy()
    print(proxy.render(doc))

    # Command for editing
    editor = Editor()
    context = DocumentContext()
    print(context.edit(editor, "New content"))

    # State for document lifecycle
    print(context.publish())
    print(context.edit(editor, "More content"))  # Should fail due to Published state

    # Event Sourcing to track changes
    store = EventStore()
    store.add_event(DocumentEvent("add_text", {"text": "Event-sourced text"}))
    store.replay(doc)
    print(doc)