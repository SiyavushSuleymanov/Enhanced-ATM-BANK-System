from datetime import datetime
from supabase import create_client

url = "https://zumeulejkljiokmfhcrk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
supabase = create_client(url, key)

class BankAccount:
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

    def transfer(self, receiver, amount):
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
        receiver_obj.balance += amount
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

    def zero(self):
        from supabase import create_client
        url = "https://zumeulejkljiokmfhcrk.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bWV1bGVqa2xqaW9rbWZoY3JrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQxMzAwNjIsImV4cCI6MjA3OTcwNjA2Mn0.oWXWPZT_aOefrnLQ4oaTFFgvI3MLHEo2MocrF492QZE"
        supabase = create_client(url, key)
        users = supabase.table("users").select("*").execute().data

        for user in users:
            supabase.table("users").update({
                "wrong_tries": 0,
                "blocked": False
            }).eq("name", user["name"]).execute()

    def update_db(self):
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
