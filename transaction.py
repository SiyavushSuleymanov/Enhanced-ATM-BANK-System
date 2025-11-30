from datetime import datetime
from supabase import create_client

url = "https://zumeulejkljiokmfhcrk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
supabase = create_client(url, key)

class BankAccount:
    def __init__(self, username, pin, balance, transactions, blocked=False):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.transactions = transactions
        self.blocked = blocked

    @classmethod
    def get_user(cls, username):
        res = supabase.table("users").select("*").eq("name", username).execute()
        if res.data:
            user = res.data[0]
            return cls(user["name"], user["pin"], user["balance"], user["transactions"], user["blocked"])
        return None

    def update_balance(self):
        supabase.table("users").update({
            "balance": self.balance,
            "transactions": self.transactions,
            "blocked": self.blocked
        }).eq("name", self.username).execute()

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(
            f"{self.username} deposited {amount} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.update_balance()
        self.update_db()
        return f"Deposit successful! Balance: {self.balance} AZN"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        self.transactions.append(
            f"{self.username} withdrew {amount} AZN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.update_balance()
        return f"Withdraw successful! Current balance: {self.balance} AZN"

    def transfer(self, receiver_name, amount):
        receiver = BankAccount.get_user(receiver_name)
        if not receiver:
            return "Receiver not found"
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        receiver.balance += amount
        self.transactions.append(
            f"{self.username} sent {amount} AZN to {receiver_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        receiver.transactions.append(
            f"received {amount} AZN from {self.username} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.update_balance()
        receiver.update_balance()
        return "Transfer successful!"

    def update_db(self):
        from supabase import create_client
        url = "https://zumeulejkljiokmfhcrk.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
        supabase = create_client(url, key)

        supabase.table("users").update({
            "balance": self.balance,
            "pin": self.pin,
            "transactions": self.transactions
        }).eq("name", self.username).execute()
