from datetime import datetime
import json
from supabase import create_client

url = "https://zumeulejkljiokmfhcrk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
supabase = create_client(url, key)

with open("userslist.json", "r") as f:
    data = json.load(f)

for u in data["users"]:
    existing = supabase.table("users").select("name").eq("name", u["name"]).execute()
    if not existing.data:
        supabase.table("users").insert({
            "name": u["name"],
            "pin": u["pin"],
            "balance": u["balance"],
            "transactions": u["transactions"],
            "wrong_tries": u["wrong_tries"],
            "blocked": u["blocked"]
        }).execute()


users = data["users"]

class BankAccount:
    def __init__(self, username: str, pin: int, balance: float, trnsct_list, wrong_tries = 0):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.trnsct_list = trnsct_list
        self.wrong_tries = wrong_tries
        self.blocked = False

    def get_user_from_db(name):
        res = supabase.table("users").select("*").eq("name", name).execute()
        if res.data:
            return res.data[0]
        return None

    def show_balance(self):
        return self.balance

    @staticmethod
    def update_balance(name, new_balance, transactions):
        supabase.table("users").update({
            "balance": new_balance,
            "transactions": transactions
        }).eq("name", name).execute()

    def transfer_money(self, receiver, amount):
        if amount > self.balance:
            return "Not enough balance"
        self.balance -= amount
        self.trnsct_list.append(
            f"{self.username} sent {amount} AZN to {receiver.username} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        receiver.balance += amount
        receiver.trnsct_list.append(
            f"{receiver.username} received {amount} AZN from {self.username} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        supabase.table("users").update({
            "balance": self.balance,
            "transactions": self.trnsct_list
        }).eq("name", self.username).execute()

        supabase.table("users").update({
            "balance": receiver.balance,
            "transactions": receiver.trnsct_list
        }).eq("name", receiver.username).execute()

        return "Transfer successful!"

    def deposit(self, amount):
        self.balance += amount
        self.trnsct_list.append(
            f"You updated your balance {amount} AZN. Your current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        BankAccount.update_balance(self.username, self.balance, self.trnsct_list)

    def withdraw_money(self, amount):
        if amount > self.balance:
            return "Your balance is too low"
        self.balance -= amount
        self.trnsct_list.append(
            f"{self.username} withdrew {amount} AZN. Your current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        supabase.table("users").update({
            "balance": self.balance,
            "transactions": self.trnsct_list
        }).eq("name", self.username).execute()

        return f"You withdrew {amount} AZN. New balance: {self.balance} AZN"

    def transaction(self):
        for tr in self.trnsct_list[:-1]:
            print(tr)
        return self.trnsct_list[-1]

'''
#LOGIN
usr = input("Enter name: ")
usr = usr.capitalize()
for i in range(len(users)):
    if usr == users[i]["name"]:
        usr = BankAccount(users[i]["name"], users[i]["pin"], users[i]["balance"], users[i]["transactions"])
        ind = i
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
print(usr.deposit_money(amount, ind))

#TRANSFERING
recvr = input("Enter receiver's name you want to transfer money to: ").capitalize()
for i in range(len(users)):
    if recvr == users[i]["name"]:
        reind = i
        recvr = BankAccount(users[i]["name"], users[i]["pin"], users[i]["balance"], users[i]["transactions"])
        trsmoney = float(input("Enter the amount of money you want to transfer: "))
        print(usr.transfer_money(recvr, trsmoney, ind, reind))
        break
    elif i == len(users) - 1:
        print("User not found!")

#WITHDRAWING
withdrawed_money = float(input("Enter money you want to withdraw: "))
print(usr.withdraw_money(withdrawed_money, ind))
'''
