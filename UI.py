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
        if page_name == "MainMenu":
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
        self.current_user_label = tk.Label(self, text="", font=("Arial", 14))
        self.current_user_label.pack(anchor="nw", padx=20, pady=10)

        self.balance_label = tk.Label(self, text="", font=("Arial", 12))
        self.balance_label.pack(anchor="nw", padx=20)

    def update_page(self):
        user = self.controller.current_user
        self.current_user_label.config(text=f"Welcome, {user["name"]}")
        self.balance_label.config(text=f"Balance: ${user["balance"]}")
class DepositPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
class TransferPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
class HistoryPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
class WithdrawPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

app = App()
app.geometry('900x500')
app.title('Enhanced ATM')
app.mainloop()

