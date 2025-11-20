from datetime import datetime
import json
import sys

with open("userslist.json", "r") as f:
    data = json.load(f)

users = data['users']


def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)


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

    def updt_balance(self, amount):
        self.balance += amount
        self.trnsct_list.append(f"{self.username} - {trsmoney} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - updated")
        print(f"{self.username}'s balance updated successfully! {self.username}'s current balance is {self.balance}")
        return f"{self.username} - {trsmoney} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - updated"

    def transfer_money(self, recvr, trsmoney):
        if trsmoney > self.balance:
            return "You don't have enough balance for this operation!"
        else:
            self.balance -= trsmoney
            self.trnsct_list.append(f"{self.username} - {trsmoney} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - taken out")
            print(f"{self.username}'s transaction successful! {self.username}'s current balance is {self.balance}")
            return f"{self.username} - {trsmoney} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - taken out"

    def deposit_money(self, amount):
        self.balance += amount
        print(f"Your current balance is {self.balance} AZN")
        self.trnsct_list.append(f"{self.balance} - {amount} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - updated")
        return f"{self.balance} - {amount} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - updated"

    def withdraw_money(self, amount):
        print(f"Your current balance is {self.balance} AZN")
        if amount > self.balance:
            return "Your balance is low"
        else:
            print("Operation was done succesfully")
            self.trnsct_list.append(f"{self.username} - {amount} - {datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))} - taken out")

    def transaction(self):
        for tr in self.trnsct_list[:-1]:
            print(tr)
        return self.trnsct_list[-1]

    def exit(self):
        print("Succeefully finished!")
        sys.exit()

'''
#LOGIN
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

#DEPOSIT
amount = float(input("Enter the amount of money you want to deposit: "))
print(usr.deposit_money(amount))

#TRANSFERING
recvr = input("Enter receiver's name you want to transfer money to: ").capitalize()
for i in range(len(users)):
    if recvr == users[i]["name"]:
        recvr = BankAccount(users[i]["name"], users[i]["pin"], users[i]["balance"], users[i]["transactions"])
        trsmoney = float(input("Enter the amount of money you want to transfer: "))
        print(usr.transfer_money(recvr, trsmoney))
        print(recvr.updt_balance(trsmoney))
        break
    elif i == len(users) - 1:
        print("User not found!")

#WITHDRAWING
withdrawed_money = float(input("Enter money you want to get: "))
print(usr.withdraw_money(withdrawed_money))

print(usr.transaction())
'''
