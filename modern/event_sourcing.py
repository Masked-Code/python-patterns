class Event:
    def __init__(self, type, amount): self.type = type; self.amount = amount

class Account:
    def __init__(self): self.events = []
    def deposit(self, amount): self.events.append(Event("deposit", amount))
    def withdraw(self, amount): self.events.append(Event("withdraw", -amount))
    def balance(self):
        return sum(event.amount for event in self.events)

account = Account()
account.deposit(100)
account.withdraw(30)
print(account.balance())  # 70