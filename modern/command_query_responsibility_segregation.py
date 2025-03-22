class PostWriteModel:
    def __init__(self): self.posts = {}
    def create_post(self, id, title): self.posts[id] = {"title": title}

class PostReadModel:
    def __init__(self, write_model): self.posts = write_model.posts
    def get_post(self, id): return self.posts.get(id, {}).get("title", "Not found")

write = PostWriteModel()
read = PostReadModel(write)
write.create_post(1, "Hello World")
print(read.get_post(1))  # Hello World