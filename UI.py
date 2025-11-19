import tkinter as tk
from tkinter import Frame

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.current_user = None
        self.frames = {}
        container = Frame(self)
        container.pack(fill='both', expand=True)
        for F in (LoginPage, MainMenu, DepositPage, TransferPage, HistoryPage, WithdrawPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("LoginPage")
    def show_frame(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(Frame):
    #from users import users, pins  #not available
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='light blue')
        self.controller = controller

        entered_username = tk.Label(self, text="Username:")
        entered_username.grid(row=2, column=0, pady=10, padx=20)
        self.entered_username = tk.Entry(self, show="*")
        self.entered_username.grid(row=2, column=1, pady=10)

        card_label = tk.Label(self, text="Card Number:")
        card_label.grid(row=0, column=0, pady=(120, 10), padx=20)
        self.card_number = tk.Entry(self)
        self.card_number.grid(row=0, column=1, pady=(120, 10))


        entered_pin = tk.Label(self, text="PIN:")
        entered_pin.grid(row=1, column=0, pady=10, padx=20)
        self.entered_pin = tk.Entry(self, show="*")
        self.entered_pin.grid(row=1, column=1, pady=10)

        # --- Login Button ---
        login_button = tk.Button(self, text="Login", command=self.login_user, width=12, height=1)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)

    def login_user(self):
        pass
class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
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

