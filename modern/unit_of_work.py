class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return f"User({self.id}, {self.name})"

class UserRepository:
    def __init__(self):
        self.users = {}
    def add(self, user):
        self.users[user.id] = user
    def get(self, id):
        return self.users.get(id)

class UnitOfWork:
    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
    def register_new(self, obj):
        self.new_objects.append(obj)
    def register_dirty(self, obj):
        self.dirty_objects.append(obj)
    def commit(self, repo):
        for obj in self.new_objects:
            repo.add(obj)
        for obj in self.dirty_objects:
            repo.add(obj) 
        self.new_objects.clear()
        self.dirty_objects.clear()

# Usage
repo = UserRepository()
uow = UnitOfWork()
user = User(1, "Bob")
uow.register_new(user)
uow.commit(repo)
print(repo.get(1))  # Output: User(1, Bob)