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
    #from users import users, pins  #not available sdsdhsdsdhsghvvbnhghjkjhghj
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        login_button = tk.Button(self, text="Login", command=self.login_user)
        login_button.grid(row=2, column=0)   #edit it
    def login_user(self):
        pass
    hbcxcxcxcxhbcxbchx
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

