import json

with open("userslist.json", "r") as f:
    data = json.load(f)

users = data['users']

class BankAccount:
    def __init__(self, username: str, pin: int, balance: float, trnsct_list):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.trnsct_list = trnsct_list

    def get_user(self):
        return f"Welcome, {self.username}"

    def show_balance(self):
        return self.balance

    def transaction(self, trnsct, amount):
        self.trnsct_list.append(trnsct)
        self.balance -= amount
        return f"Transaction successful! Your current balance is {self.balance}"

    def updt_balance(self, amount):
        self.balance += amount
        return f"Balance updated successfully! Your current balance is {self.balance}"

usr = input("Enter name: ")
usr = usr.capitalize()
for i in range(len(users)):
    if usr == users[i]["name"]:
        usr = BankAccount(users[i]["name"], users[i]["pin"], users[i]["balance"], users[i]["transactions"])
        pin = int(input(f"{usr.get_user()}. Enter your PIN: "))
        if pin == users[i]["pin"]:
            print(f"Welcome to your Bank Account. Your current balance is {usr.show_balance()}")
        else:
            print("Incorrect PIN")
        break
    elif i == len(users)-1:
        print("User not found!")





