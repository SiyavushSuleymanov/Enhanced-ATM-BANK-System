import datetime
import tkinter as tk
from tkinter import Frame
from transaction import BankAccount, users


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
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        for j in range(10):
            self.grid_columnconfigure(j, weight=1)
        entered_username = tk.Label(self, text="Username:", font=("Arial", 24, "bold"), bg="#f0f0f0")
        entered_username.grid(row=3, column=1, columnspan=4, sticky="e", padx=10, pady=10)
        self.usr = tk.Entry(self, font=("Arial", 24))
        self.usr.grid(row=3, column=5, columnspan=4, sticky="w", padx=10, pady=10)
        pin = tk.Label(self, text="PIN:", font=("Arial", 24, "bold"), bg="#f0f0f0")
        pin.grid(row=4, column=1, columnspan=4, sticky="e", padx=10, pady=10)
        self.entered_pin = tk.Entry(self, font=("Arial", 24), show="*")
        self.entered_pin.grid(row=4, column=5, columnspan=4, sticky="w", padx=10, pady=10)
        login_button = tk.Button(self, text="Login", command=self.login_user,font=("Arial", 24, "bold"), width=15, height=2)
        login_button.grid(row=5, column=1, columnspan=8, pady=30)
    def login_user(self):
        from transaction import users
        usr = self.usr.get().capitalize()
        pin = int(self.entered_pin.get())
        for current_user_ind in range(len(users)):
            if usr == users[current_user_ind]["name"]:
                usr = BankAccount(users[current_user_ind]["name"], users[current_user_ind]["pin"], users[current_user_ind]["balance"], users[current_user_ind]["transactions"])
                self.current_user_ind = current_user_ind
                if pin == users[current_user_ind]["pin"]:
                    self.controller.current_user = usr
                    self.controller.show_frame("MainMenu")
                else:
                    passwd_error = tk.Label(self, text="Incorrect PIN", fg="red")
                    passwd_error.grid(row=5, column=7, columnspan=2, pady=10)
                break
            elif current_user_ind == len(users) - 1:
                self.controller.current_user = None
                self.controller.show_frame("LoginPage")


    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")



class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        self.grid_rowconfigure(0, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.grid_columnconfigure(j, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.current_user_label = tk.Label(self, text="", font=("Arial", 40, "bold"), bg="#f0f0f0")
        self.current_user_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")
        button_font = ("Arial", 24, "bold")
        button_width = 15
        button_height = 2
        self.deposit_button = tk.Button(self, text="Deposit", width=button_width, height=button_height,font=button_font, command=lambda: controller.show_frame("DepositPage"))
        self.deposit_button.grid(row=2, column=1, pady=10, padx=20, sticky="w")
        self.withdraw_button = tk.Button(self, text="Withdraw", width=button_width, height=button_height,font=button_font, command=lambda: controller.show_frame("WithdrawPage"))
        self.withdraw_button.grid(row=3, column=1, pady=10, padx=20, sticky="w")
        self.transfer_button = tk.Button(self, text="Transfer", width=button_width, height=button_height,font=button_font, command=lambda: controller.show_frame("TransferPage"))
        self.transfer_button.grid(row=2, column=1, pady=10, padx=20, sticky="e")
        self.history_button = tk.Button(self, text="History", width=button_width, height=button_height,font=button_font, command=lambda: controller.show_frame("HistoryPage"))
        self.history_button.grid(row=3, column=1, pady=10, padx=20, sticky="e")
        self.logout_button = tk.Button(self, text="Logout", width=button_width, height=button_height, font=button_font, command=self.logout)
        self.logout_button.grid(row=6, column=1, columnspan=3, pady=20, sticky="w")

    def update_page(self):
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=f"Welcome, {user.username}")
        else:
            self.current_user_label.config(text="Welcome, Guest")

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
        self.deposit_button = tk.Button(self, text="Deposit", width=12, command=lambda: BankAccount.deposit_money(self.controller.current_user, float(self.amount.get()),self.current_user_ind))
        self.deposit_button.grid(row=4, column=0, pady=10, padx=20)


    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")



    def update_page(self):
        user = self.controller.current_user
        if user:
            from transaction import users
            for i in range(len(users)):
                if users[i]["name"] == user.username:
                    self.current_user_ind = i
                    break
            self.current_user_label.config(text=f"Welcome, {user.username}")
            self.balance_label.config(text="Balance: $******")
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

        tk.Button(self, text="Show Balance", command=self.show_balance_func).grid(
            row=1, column=1, padx=10, pady=5, sticky="w"
        )

        tk.Button(self, text="Main Menu", width=12,
                  command=lambda: controller.show_frame("MainMenu")).grid(
            row=9, column=0, pady=200, padx=20
        )

        tk.Label(self, text="Transfer Amount: ").grid(row=3, column=0, padx=20, pady=20)
        self.trsmoney = tk.Entry(self)
        self.trsmoney.grid(row=3, column=1, padx=20, pady=20)

        tk.Label(self, text="Receiver Username: ").grid(row=4, column=0, padx=20, pady=20)

        self.recvr_var = tk.StringVar()
        self.recvr_var.trace("w", self.check_receiver)
        self.recvr = tk.Entry(self, textvariable=self.recvr_var)
        self.recvr.grid(row=4, column=1, padx=20, pady=20)

        self.receiver_status = tk.Label(self, text="", fg="red")
        self.receiver_status.grid(row=4, column=2, padx=10)

        self.transfer_button = tk.Button(self, text="Transfer", width=12, command= self.transfer_action)
        self.transfer_button.grid(row=5, column=0, pady=10, padx=20)
        self.transfer_button.config(state="disabled")

    def transfer_action(self):
        from transaction import users
        sender = self.controller.current_user
        receiver_name = self.recvr.get().capitalize()
        amount = float(self.trsmoney.get())
        sender_ind = None
        receiver_ind = None
        for i, u in enumerate(users):
            if u["name"] == sender.username:
                sender_ind = i
            if u["name"] == receiver_name:
                receiver_ind = i
        if sender_ind is None or receiver_ind is None:
            self.receiver_status.config(text="User not found!", fg="red")
            return
        result = sender.transfer_money(recvr=receiver_name, trsmoney=amount, ind=sender_ind, reind = receiver_ind)
        self.balance_label.config(text=f"Balance: ${sender.balance}")
        self.receiver_status.config(text="Transfer Successful", fg="green")
        print(result)

    def update_page(self):
        user = self.controller.current_user
        self.current_user_label.config(text=f"Welcome, {user.username}")
        self.balance_label.config(text=f"Balance: $******")

    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")

    def check_receiver(self, *args):
        recvr = self.recvr_var.get().capitalize()
        if recvr == "":
            self.receiver_status.config(text="")
            self.transfer_button.config(state="disabled")
            return
        for u in users:
            if u["name"] == recvr:
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
        self.back_button = tk.Button(self,text="Back",command=lambda: self.controller.show_frame("MainMenu"))
        self.back_button.pack(pady=20)

    def update_page(self):
        self.list_box.delete(0, tk.END)
        for item in self.controller.current_user.trnsct_list:
            self.list_box.insert(tk.END, item)




class WithdrawPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.enter_money_label = tk.Label(self, text = "Enter the amount you want to withdraw")
        self.enter_money_label.grid( row = 0 , column = 2, pady=20)
        self.amount = tk.Entry(self)
        self.amount.grid(row = 0 , column = 3, pady=20)
        for user_ind in range(len(users)):
            if users[user_ind]["name"] == self.controller.current_user:
                ind = user_ind
                break
        self.balance_label = tk.Label(self, text =f"Balance: ${users[user_ind]['balance']}")
        self.balance_label.grid(row = 1, column = 2, pady=20)
        self.update_balance_button = tk.Button(self, text="Show Balance", command=self.show_balance_func)
        self.update_balance_button.grid(row = 1, column = 3, pady=20)
        tk.Button(self, text="Withdraw",command= self.withdraw_action).grid(row = 2, column = 2,pady=20)
        self.back_button = tk.Button(self, text="Back", command = lambda:self.controller.show_frame("MainMenu"))
        self.back_button.grid(row = 9, column = 2, pady=20)

    def withdraw_action(self):
        user = self.controller.current_user
        amount = float(self.amount.get())
        user_ind = None
        for i, u in enumerate(users):
            if u["name"] == user.username:
                user_ind = i
        result = user.withdraw_money(amount, user_ind)
        print(result)
    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")



app = App()
app.geometry('1920x1080')
app.title('Enhanced ATM')
app.mainloop()

