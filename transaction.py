from datetime import datetime
from supabase import create_client

"""A module for managing bank account transactions using Supabase as the backend.
    All datas are stored in Supabase database.(online postgresql database)"""

url = "https://zumeulejkljiokmfhcrk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
supabase = create_client(url, key)
"""this part is for connecting to supabase database. You need url and anon key for this connection."""


class BankAccount:
    """A class representing a bank account with methods for deposit, withdrawal, and transfer.
           self.attributes: (declared all of them in __init__ method)
    """
    def __init__(self, username, pin, balance, transactions, blocked=False,wrong_tries=0):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.transactions = transactions
        self.blocked = blocked
        self.wrong_tries = wrong_tries

    @classmethod
    def get_user(cls, username):
        res = supabase.table("users").select("*").eq("name", username).execute()
        if res.data:
            user = res.data[0]
            return cls(user["name"], user["pin"], user["balance"], user["transactions"], user["blocked"],user["wrong_tries"])
        return None

    def update_balance(self):
        """After each transaction, we need to update balance in our database.
                   This method updates the balance and transactions in the Supabase database.
                   """
        supabase.table("users").update({
            "balance": self.balance,
            "transactions": self.transactions,
            "blocked": self.blocked
        }).eq("name", self.username).execute()

    def deposit(self, amount):
        """Deposit money into the account.
                    Adding float conversion to ensure two decimal places for balance.
                    After transaction, we call agaiin update_balance method for updating balance in database."""
        self.balance += amount
        self.balance = float(f"{self.balance:.2f}")
        self.transactions.append(
            f"{self.username} deposited {amount} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.update_balance()
        self.update_db()
        return f"Deposit successful! Balance: {self.balance} AZN"

    def withdraw(self, amount):
        """Withdraw money from the account.
                   Adding float conversion to ensure two decimal places for balance.
                   After transaction, we call agaiin update_balance method for updating balance in database.
                   Main point is checking if there is enough balance for withdrawal."""
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        self.balance = float(f"{self.balance:.2f}")
        self.transactions.append(
            f"{self.username} withdrew {amount} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.update_balance()
        return f"Withdraw successful! Current balance: {self.balance} AZN"

    def transfer(self, receiver, amount):
        """Transfer money to another account.
                    Receiver can be either a username (str) or a BankAccount object.
                    Adding float conversion to ensure two decimal places for balance.
                    After transaction, we call agaiin update_balance method for updating balance in database.
                    Also, we return timestamp for transaction recording for history"""
        if isinstance(receiver, str):
            receiver_obj = BankAccount.get_user(receiver)
        else:
            receiver_obj = receiver
        if not receiver_obj:
            return "Receiver not found"
        if amount > self.balance:
            return "Insufficient funds!"
        if receiver_obj.username == self.username:
            return "Cannot transfer to self"
        self.balance -= amount
        self.balance = float(f"{self.balance:.2f}")
        receiver_obj.balance += amount
        receiver_obj.balance = float(f"{receiver_obj.balance:.2f}")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transactions.append(
            f"{self.username} sent {amount} AZN to {receiver_obj.username} - {timestamp}"
        )
        receiver_obj.transactions.append(
            f"{receiver_obj.username} received {amount} AZN from {self.username} - {timestamp}"
        )
        try:
            self.update_balance()
        except Exception:
            pass
        try:
            receiver_obj.update_balance()
        except Exception:
            pass
        return "Transfer successful!"

    def update_db(self):
        """for updating all attributes of user in database.
                """
        from supabase import create_client
        url = "https://zumeulejkljiokmfhcrk.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
        supabase = create_client(url, key)

        supabase.table("users").update({
            "balance": self.balance,
            "pin": self.pin,
            "transactions": self.transactions,
            "wrong_tries": self.wrong_tries,
            "blocked": self.blocked
        }).eq("name", self.username).execute()
