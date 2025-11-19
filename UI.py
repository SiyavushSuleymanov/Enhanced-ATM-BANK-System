import datetime
import tkinter as tk
from tkinter import Frame

from users import BankAccount


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.current_user = None
        self.frames = {}
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (LoginPage, MainMenu, DepositPage, TransferPage, HistoryPage, WithdrawPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("LoginPage")
    def show_frame(self,page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "update_page"):
            frame.update_page()
        frame.tkraise()

class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        for i in range(20):
            self.grid_rowconfigure(i, weight=1)
        for j in range(20):
            self.grid_columnconfigure(j, weight=1)

        entered_username = tk.Label(self, text="Username:")
        entered_username.grid(row=2, column=6, pady=10, padx=20)
        self.entered_username = tk.Entry(self)
        self.entered_username.grid(row=2, column=7, pady=10)

        entered_pin = tk.Label(self, text="PIN:")
        entered_pin.grid(row=3, column=6, pady=10, padx=20)
        self.entered_pin = tk.Entry(self, show="*")
        self.entered_pin.grid(row=3, column=7, pady=10)


        login_button = tk.Button(self, text="Login", command=self.login_user, width=12, height=1)
        login_button.grid(row=4, column=7, columnspan=2, pady=30)

    def login_user(self):
        from users import users
        username = self.entered_username.get()
        pin = self.entered_pin.get()
        print("Entered username:", username)
        print("Entered PIN:", pin)
        if pin == "":
            print("PIN is empty")
            return
        try:
            pin = int(pin)
        except:
            print("PIN is not a number")
            return
        found_user = None
        for u in users:
            if username == u["name"]:
                found_user = u
                break
        if not found_user:
            print("User not found in users.py")
            return
        print("User found:", found_user["name"])
        if pin == found_user["pin"]:
            self.controller.current_user = BankAccount(
                found_user["name"],
                found_user["pin"],
                found_user["balance"],
                found_user["transactions"]
            )
            self.controller.show_frame("MainMenu")
        else:
            print("PIN is incorrect!")


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_user_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.current_user_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.balance_label = tk.Label(self, text="", font=("Arial", 12))
        self.balance_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.update_balance_button = tk.Button(self, text="Show Balance", command=self.show_balance_func)
        self.update_balance_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.deposit_button = tk.Button(self, text="Deposit", width=12,command=lambda: controller.show_frame("DepositPage"))
        self.deposit_button.grid(row=2, column=0, pady=10, padx=20)

        self.withdraw_button = tk.Button(self, text="Withdraw", width=12,command=lambda: controller.show_frame("WithdrawPage"))
        self.withdraw_button.grid(row=3, column=0, pady=10, padx=20)

        self.transfer_button = tk.Button(self, text="Transfer", width=12, command=lambda: controller.show_frame("TransferPage"))
        self.transfer_button.grid(row=4, column=0, pady=10, padx=20)

        self.history_button = tk.Button(self, text="History", width=12, command=lambda: controller.show_frame("HistoryPage"))
        self.history_button.grid(row=5, column=0, pady=10, padx=20)

        self.logout_button = tk.Button(self, text="Logout", width=12, command=self.logout)
        self.logout_button.grid(row=6, column=0, pady=10, padx=20)

    def update_page(self):
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=f"Welcome, {user.username}")
            self.balance_label.config(text=f"Balance: $******")
        else:
            self.current_user_label.config(text="Welcome, Guest")
            self.balance_label.config(text="Balance: $0")

    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")

class DepositPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_user_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.current_user_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.balance_label = tk.Label(self, text="", font=("Arial", 12))
        self.balance_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.update_balance_button = tk.Button(self, text="Show Balance", command=self.show_balance_func)
        self.update_balance_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")


        self.MainMenu_button = tk.Button(self, text="Main Menu", width=12, command=lambda: controller.show_frame("MainMenu"))
        self.MainMenu_button.grid(row=9, column=0, pady=200, padx=20)

        tk.Label(self, text="Deposit Amount: ").grid(row=3, column=0, padx=20, pady=20)
        self.amount = tk.Entry(self)
        self.amount.grid(row=3, column=1, padx=20, pady=20)

        from transaction import BankAccount
        self.deposit_button = tk.Button(self, text="Deposit", width=12, command=lambda: BankAccount.deposit_money(self.controller.current_user, float(self.amount.get())))
        self.deposit_button.grid(row=4, column=0, pady=10, padx=20)

    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")

    def update_page(self):
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=f"Welcome, {user.username}")
            self.balance_label.config(text=f"Balance: $******")
        else:
            self.current_user_label.config(text="Welcome, Guest")
            self.balance_label.config(text="Balance: $0")

class TransferPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_user_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        self.current_user_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.balance_label = tk.Label(self, text="", font=("Arial", 12))
        self.balance_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.update_balance_button = tk.Button(self, text="Show Balance", command=self.show_balance_func)
        self.update_balance_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.MainMenu_button = tk.Button(
            self, text="Main Menu", width=12,
            command=lambda: controller.show_frame("MainMenu")
        )
        self.MainMenu_button.grid(row=9, column=0, pady=200, padx=20)

        tk.Label(self, text="Transfer Amount: ").grid(row=3, column=0, padx=20, pady=20)
        self.trsmoney = tk.Entry(self)
        self.trsmoney.grid(row=3, column=1, padx=20, pady=20)

        tk.Label(self, text="Receiver Username: ").grid(row=4, column=0, padx=20, pady=20)

        # Track receiver live check
        self.recvr_var = tk.StringVar()
        self.recvr_var.trace("w", self.check_receiver)

        self.recvr = tk.Entry(self, textvariable=self.recvr_var)
        self.recvr.grid(row=4, column=1, padx=20, pady=20)

        self.receiver_status = tk.Label(self, text="", fg="red")
        self.receiver_status.grid(row=4, column=2, padx=10)

        from users import BankAccount
        self.transfer_button = tk.Button(
            self, text="Transfer", width=12,
            command=lambda: BankAccount.transfer_money(
                self.controller.current_user,
                self.recvr.get(),
                float(self.trsmoney.get())
            )
        )
        self.transfer_button.grid(row=5, column=0, pady=10, padx=20)


    def update_page(self):
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=f"Welcome, {user.username}")
            self.balance_label.config(text=f"Balance: $******")
        else:
            self.current_user_label.config(text="Welcome, Guest")
            self.balance_label.config(text="Balance: $0")

    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")


    def check_receiver(self, *args):
        from users import users
        name = self.recvr_var.get()
        if name == "":
            self.receiver_status.config(text="")
            return

        for u in users:
            if u["name"] == name:
                self.receiver_status.config(text="✓ User found", fg="green")
                self.transfer_button.config(state="normal")
                return
        self.receiver_status.config(text="✗ User not found", fg="red")
        self.transfer_button.config(state="disabled")


class HistoryPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.list_box = tk.Listbox(self, width=50, height=15)
        self.list_box.pack(pady=20)


    def update_page(self):
        for w in self.winfo_children():
            w.destroy()
        tk.Label(self, text="Transaction History", font=("Arial", 16)).pack(pady=10)
        history_list = self.controller.current_user.trnsct_list
        if not history_list:
            tk.Label(self, text="No transactions found.").pack(pady=10)
        else:
            for item in history_list:
                tk.Label(self, text=item).pack(anchor="w")
        tk.Button(self, text="Back",command=lambda: self.controller.show_frame("MainMenu")).pack(pady=20)




class WithdrawPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

app = App()
app.geometry('900x500')
app.title('Enhanced ATM')
app.mainloop()

