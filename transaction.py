
from datetime import datetime
import json
import sys

from supabase import create_client

url = "https://zumeulejkljiokmfhcrk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"

supabase = create_client(url, key)

# Users select
response = supabase.table("users").select("*").execute()
users = response.data


class BankAccount:
    def __init__(self, username: str, pin: int, balance: float, trnsct_list, wrong_tries = 0):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.trnsct_list = trnsct_list
        self.wrong_tries = wrong_tries
        self.blocked = False

    def get_user(self):
        return self.username

    def show_balance(self):
        return self.balance

    def updt_balance(self, amount, ind):
        self.balance += amount
        users[ind]["balance"] = self.balance
        self.trnsct_list.append(
            f"{self.username} updated {amount} AZN. {self.username}'s current balance {self.balance} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        supabase.table("users").update({"balance": new_balance, "transactions": new_list}).eq("name", user).execute()

        return f"{self.username} updated {amount} AZN. Current balance {self.balance} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def transfer_money(self, recvr, trsmoney, ind, reind):
        from datetime import datetime
        import json

        if trsmoney > users[ind]["balance"]:
            return "You don't have enough balance!"
        self.balance -= trsmoney
        supabase.table("users").update({"balance": users[ind]["balance"]}).eq("name", sender_name).execute()
        supabase.table("users").update({"balance": users[reind]["balance"]}).eq("name", receiver_name).execute()
        supabase.table("users").update({
            "transactions": users[ind]["transactions"] + [new_transaction]
        }).eq("name", sender_name).execute()

        supabase.table("users").update({"balance": new_balance, "transactions": new_list}).eq("name", user).execute()

        return "Transfer successful!"



    def deposit_money(self, amount, ind):
        self.balance += amount
        users[ind]["balance"] = self.balance
        self.trnsct_list.append(f"You updated your balance {amount} AZN. Your current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        supabase.table("users").update({"balance": new_balance, "transactions": new_list}).eq("name", user).execute()

        return f"You updated your balance {amount} AZN. Your current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def withdraw_money(self, amount, ind):
        if amount > self.balance:
            return "Your balance is low"
        else:
            self.balance -= amount
            users[ind]["balance"] = self.balance
            print("Operation was done succesfully")
            self.trnsct_list.append(
                f"{self.username} took out {amount} AZN. Your current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            supabase.table("users").update({"balance": new_balance, "transactions": new_list}).eq("name",
                                                                                                  user).execute()

            return f"{self.username} took out {amount} AZN. {self.username}'s current balance {self.balance} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def transaction(self):
        for tr in self.trnsct_list[:-1]:
            print(tr)
        return self.trnsct_list[-1]

    def exit(self):
        print("Successfully finished!")
        sys.exit()

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
