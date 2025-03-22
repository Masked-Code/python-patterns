class ChatRoom:
    def show_message(self, user, message): return f"{user} says: {message}"

class User:
    def __init__(self, name, chatroom): self.name = name; self.chatroom = chatroom
    def send(self, message): return self.chatroom.show_message(self.name, message)

chat = ChatRoom()
user1 = User("Alice", chat)
print(user1.send("Hi!"))  # Alice says: Hi!