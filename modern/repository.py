class User:
    def __init__(self, id, name): self.id = id; self.name = name
    def __str__(self): return f"User({self.id}, {self.name})"

class UserRepository:
    def __init__(self): self.users = {}
    def add(self, user): self.users[user.id] = user
    def get(self, id): return self.users.get(id)

repo = UserRepository()
repo.add(User(1, "Alice"))
user = repo.get(1)
print(user)  # User(1, Alice)