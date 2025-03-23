from abc import ABC, abstractmethod
import threading
from typing import List, Dict, Optional
import time
import uuid

# Creational Pattern: Abstract Factory
# Creates families of related objects (Task and TaskUI)
class TaskFactory(ABC):
    @abstractmethod
    def create_task(self, description: str) -> 'Task':
        pass

    @abstractmethod
    def create_task_ui(self) -> 'TaskUI':
        pass

class SimpleTaskFactory(TaskFactory):
    def create_task(self, description: str) -> 'Task':
        return SimpleTask(description)

    def create_task_ui(self) -> 'TaskUI':
        return ConsoleTaskUI()

class PriorityTaskFactory(TaskFactory):
    def create_task(self, description: str) -> 'Task':
        return PriorityTask(description)

    def create_task_ui(self) -> 'TaskUI':
        return FancyTaskUI()

# Creational Pattern: Prototype
# Clones existing tasks to create new ones
class Task(ABC):
    def __init__(self, description: str):
        self.description = description
        self.id = str(uuid.uuid4())

    @abstractmethod
    def clone(self) -> 'Task':
        pass

    @abstractmethod
    def execute(self):
        pass

class SimpleTask(Task):
    def clone(self) -> 'Task':
        return SimpleTask(self.description)

    def execute(self):
        print(f"Executing simple task: {self.description}")

class PriorityTask(Task):
    def __init__(self, description: str):
        super().__init__(description)
        self.priority = 1

    def clone(self) -> 'Task':
        new_task = PriorityTask(self.description)
        new_task.priority = self.priority
        return new_task

    def execute(self):
        print(f"Executing priority task: {self.description} (Priority: {self.priority})")

# Structural Pattern: Bridge
# Separates task abstraction from its UI implementation
class TaskUI(ABC):
    @abstractmethod
    def display(self, task: Task):
        pass

class ConsoleTaskUI(TaskUI):
    def display(self, task: Task):
        print(f"Console UI: {task.description}")

class FancyTaskUI(TaskUI):
    def display(self, task: Task):
        print(f"Fancy UI: *** {task.description} ***")

class TaskManager:
    def __init__(self, ui: TaskUI):
        self.tasks: List[Task] = []
        self.ui = ui

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.ui.display(task)

# Structural Pattern: Flyweight
# Shares common task metadata to save memory
class TaskMetadata:
    _shared_metadata = {}

    def __init__(self, category: str):
        self.category = category

    @classmethod
    def get_metadata(cls, category: str) -> 'TaskMetadata':
        if category not in cls._shared_metadata:
            cls._shared_metadata[category] = TaskMetadata(category)
        return cls._shared_metadata[category]

class TaskWithMetadata(Task):
    def __init__(self, description: str, category: str):
        super().__init__(description)
        self.metadata = TaskMetadata.get_metadata(category)

    def clone(self) -> 'Task':
        return TaskWithMetadata(self.description, self.metadata.category)

    def execute(self):
        print(f"Task: {self.description} in category {self.metadata.category}")

# Behavioral Pattern: Chain of Responsibility
# Handles task approval through a chain of validators
class TaskValidator(ABC):
    def __init__(self):
        self.next_validator: Optional[TaskValidator] = None

    def set_next(self, validator: 'TaskValidator') -> 'TaskValidator':
        self.next_validator = validator
        return validator

    @abstractmethod
    def validate(self, task: Task) -> bool:
        pass

class DescriptionValidator(TaskValidator):
    def validate(self, task: Task) -> bool:
        if not task.description:
            print("Validation failed: Empty description")
            return False
        if self.next_validator:
            return self.next_validator.validate(task)
        return True

class PriorityValidator(TaskValidator):
    def validate(self, task: Task) -> bool:
        if isinstance(task, PriorityTask) and task.priority < 0:
            print("Validation failed: Negative priority")
            return False
        if self.next_validator:
            return self.next_validator.validate(task)
        return True

# Behavioral Pattern: Mediator
# Coordinates task execution between components
class TaskMediator:
    def __init__(self):
        self.task_manager = None
        self.validator = None

    def set_task_manager(self, manager: TaskManager):
        self.task_manager = manager

    def set_validator(self, validator: TaskValidator):
        self.validator = validator

    def process_task(self, task: Task):
        if self.validator.validate(task):
            self.task_manager.add_task(task)
            task.execute()

# Behavioral Pattern: Visitor
# Adds external operations (e.g., reporting) to tasks
class TaskVisitor(ABC):
    @abstractmethod
    def visit_simple_task(self, task: SimpleTask):
        pass

    @abstractmethod
    def visit_priority_task(self, task: PriorityTask):
        pass

class ReportVisitor(TaskVisitor):
    def visit_simple_task(self, task: SimpleTask):
        print(f"Report: Simple task {task.id} - {task.description}")

    def visit_priority_task(self, task: PriorityTask):
        print(f"Report: Priority task {task.id} - {task.description} (P: {task.priority})")

class TaskWithVisitor(Task):
    def accept(self, visitor: TaskVisitor):
        pass

class SimpleTask(SimpleTask, TaskWithVisitor):
    def accept(self, visitor: TaskVisitor):
        visitor.visit_simple_task(self)

class PriorityTask(PriorityTask, TaskWithVisitor):
    def accept(self, visitor: TaskVisitor):
        visitor.visit_priority_task(self)

# Modern Pattern: Saga (Simplified)
# Manages distributed task workflows with compensation
class TaskSaga:
    def __init__(self):
        self.steps = []
        self.compensations = []

    def add_step(self, step, compensation):
        self.steps.append(step)
        self.compensations.append(compensation)

    def execute(self):
        for i, step in enumerate(self.steps):
            try:
                step()
            except Exception as e:
                print(f"Step {i} failed: {e}")
                for comp in reversed(self.compensations[:i]):
                    comp()
                return False
        return True

# Main execution
if __name__ == "__main__":
    # Abstract Factory
    factory = PriorityTaskFactory()
    task = factory.create_task("High priority task")
    ui = factory.create_task_ui()

    # Prototype
    cloned_task = task.clone()
    cloned_task.priority = 5

    # Bridge
    manager = TaskManager(ui)

    # Flyweight
    task_with_meta = TaskWithMetadata("Review code", "Development")

    # Chain of Responsibility
    desc_validator = DescriptionValidator()
    prio_validator = PriorityValidator()
    desc_validator.set_next(prio_validator)

    # Mediator
    mediator = TaskMediator()
    mediator.set_task_manager(manager)
    mediator.set_validator(desc_validator)

    # Visitor
    reporter = ReportVisitor()
    task.accept(reporter)
    cloned_task.accept(reporter)

    # Saga
    saga = TaskSaga()
    saga.add_step(
        lambda: mediator.process_task(task),
        lambda: print("Compensating: Removing task")
    )
    saga.add_step(
        lambda: mediator.process_task(cloned_task),
        lambda: print("Compensating: Undoing cloned task")
    )
    saga.execute()