import datetime
import tkinter as tk
from tkinter import Frame, ttk

from transaction import BankAccount, users


PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#6c757d"
SUCCESS_COLOR = "#28a745"
DANGER_COLOR = "#dc3545"
BACKGROUND_COLOR = "#f7f7f7"
FOREGROUND_COLOR = "#333333"

MAIN_FONT = ("Helvetica", 20)
TITLE_FONT = ("Helvetica", 30, "bold")
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.current_user = None
        self.frames = {}
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background="white")
        self.style.configure('TLabel', background="white", font=MAIN_FONT, foreground=FOREGROUND_COLOR)
        self.style.configure('Title.TLabel', font=TITLE_FONT, foreground=PRIMARY_COLOR)
        self.style.configure('SubTitle.TLabel', font=("Segoe UI", 20, "bold"), foreground=FOREGROUND_COLOR)
        self.style.configure('Primary.TButton', font=("Segoe UI", 16, "bold"), background=PRIMARY_COLOR,
                             foreground="white", borderwidth=0, relief="flat", padding=15)
        self.style.map('Primary.TButton', background=[('active', '#0056b3')])
        self.style.configure('Success.TButton', font=("Segoe UI", 16, "bold"), background=SUCCESS_COLOR,
                             foreground="white", borderwidth=0, relief="flat", padding=15)
        self.style.map('Success.TButton', background=[('active', '#1e7e34')])
        self.style.configure('Danger.TButton', font=("Segoe UI", 16, "bold"), background=DANGER_COLOR,
                             foreground="white", borderwidth=0, relief="flat", padding=15)
        self.style.map('Danger.TButton', background=[('active', '#c82333')])
        self.style.configure('Secondary.TButton', font=("Segoe UI", 14), background=SECONDARY_COLOR, foreground="white",
                             borderwidth=0, relief="flat", padding=10)
        self.style.map('Secondary.TButton', background=[('active', '#5a6268')])
        self.style.configure('TEntry', font=MAIN_FONT, padding=5, fieldbackground="white")
        try:
            image_path = "ufaz_vector_bg.png"
            original_image = Image.open(image_path)
            resized_image = original_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self, image=self.bg_image)
            background_label.image = self.bg_image
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            container = Frame(self)
        except FileNotFoundError:
            print(f"WARNING: Image {image_path} not found. Using default background.")
            container = Frame(self, bg=BACKGROUND_COLOR)
        except Exception as e:
            print(f"ERROR: A problem occurred while loading the image: {e}")
            container = Frame(self, bg=BACKGROUND_COLOR)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (LoginPage, MainMenu, DepositPage, TransferPage, HistoryPage, WithdrawPage, LoadingPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("LoginPage")
    def show_frame(self, page_name, transition_time_ms=0):
        if transition_time_ms > 0:
            loading_frame = self.frames["LoadingPage"]
            if hasattr(loading_frame, "update_page"):
                loading_frame.update_page()
            loading_frame.tkraise()
            def switch_to_target():
                frame = self.frames[page_name]
                if hasattr(frame, "update_page"):
                    frame.update_page()
                frame.tkraise()
            self.after(transition_time_ms, switch_to_target)
        else:
            frame = self.frames[page_name]
            if hasattr(frame, "update_page"):
                frame.update_page()
            frame.tkraise()

class LoadingPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(5): self.grid_rowconfigure(i, weight=1)
        for j in range(5): self.grid_columnconfigure(j, weight=1)
        ttk.Label(self, text="Processing Transaction...",
                  font=("Segoe UI", 24, "bold"),
                  foreground=PRIMARY_COLOR).grid(row=1, column=2, padx=50, pady=(50, 10))
        self.spinner = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.spinner.grid(row=2, column=2, padx=50, pady=20)
        ttk.Label(self, text="Redirecting to Login...",
                  font=("Segoe UI", 14),
                  foreground=SECONDARY_COLOR).grid(row=3, column=2, padx=50, pady=(10, 50))
    def update_page(self):
        self.spinner.start(10)

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(10): self.grid_columnconfigure(j, weight=1)
        title = ttk.Label(self, text="UFAZ BANK 💳", style='Title.TLabel')
        title.grid(row=1, column=1, columnspan=8, pady=50, sticky="n")
        entered_username = ttk.Label(self, text="Username :", font=("Segoe UI", 20, "bold"))
        entered_username.grid(row=3, column=2, columnspan=3, sticky="e", padx=10, pady=20)
        self.usr = ttk.Entry(self, style='TEntry',font=("Helvetica", 16, "bold"))
        self.usr.focus_set()
        self.usr.grid(row=3, column=5, columnspan=3, sticky="w", padx=10, pady=20)
        self.usr.bind("<Return>", self.login_user)
        pin = ttk.Label(self, text="PIN :", font=("Segoe UI", 18, "bold"))
        pin.grid(row=4, column=2, columnspan=3, sticky="e", padx=10, pady=20)
        login_button = ttk.Button(self, text="Login", command=self.login_user, style='Primary.TButton')
        login_button.grid(row=5, column=2, columnspan=6, pady=40, sticky="ew")
        self.error_label = ttk.Label(self, text="", foreground=DANGER_COLOR, background="white")
        self.error_label.grid(row=6, column=2, columnspan=6, pady=5, sticky="n")
        self.pin = ""
    def login_user(self, k=0):
        self.usr.config(state="disabled")
        # WORKING ON...
        pin_len = 4
        def pressed(ent_digit):
            if ent_digit.keysym.isdigit() and len(str(self.pin)) != 4:
                self.pin += ent_digit.keysym
                upgrade()
                if upgrade() == 1:
                    self.pin = self.pin[:4] # OUR ENTERED 4-digit PIN - (result)
                    self.l = True
                    # print(int(self.pin))
                    return 0
            elif ent_digit.keysym == "BackSpace":
                if type(self.pin) == str:
                    delete()
                    self.pin = self.pin[:-1]
                elif type(self.pin) == int:
                    pass

        def upgrade(): # Upgrades dot list
            try:
                if len(self.pin) <= pin_len:
                    dot_list[len(self.pin) - 1].config(text='◉', font=("Arial", 30), foreground="blue")
                if len(self.pin) == pin_len:
                    return 1
            except IndexError:
                pass

        def delete():
            if len(self.pin) <= pin_len:
                dot_list[len(self.pin) - 1].config(text='〇', font=("Arial", 30), foreground="blue")

        frm = ttk.Frame(self)
        frm.grid(row=4, column=3, columnspan=5, padx=10, pady=20)
        dot_list = []
        for _ in range(pin_len):
            dot = ttk.Label(frm, text='〇', font=('Arial', 30), foreground="blue")
            dot.pack(side="left")
            dot_list.append(dot)

        self.focus_set()
        self.bind('<Key>', pressed)
        # WORKING ON...

        usr_input = self.usr.get().capitalize()
        from transaction import users
        self.error_label.config(text="")
        user_found = False
        for current_user_ind in range(len(users)):
            user_data = users[current_user_ind]
            if usr_input == user_data["name"]:
                user_found = True
                usr = BankAccount(user_data["name"], user_data["pin"], user_data["balance"], user_data["transactions"],
                                  user_data["wrong_tries"])
                usr.blocked = user_data["blocked"]
                self.current_user_ind = current_user_ind
                if usr.blocked:
                    self.error_label.config(text="❌ Card is blocked", foreground=DANGER_COLOR)
                    return
                try:
                    if int(self.pin) == user_data["pin"]:
                        users[current_user_ind]["wrong_tries"] = 0
                        self.controller.current_user = usr
                        self.usr.delete(0, tk.END)
                        self.controller.show_frame("MainMenu", transition_time_ms=1500)
                    else:
                        users[current_user_ind]["wrong_tries"] += 1
                        if users[current_user_ind]["wrong_tries"] < 3:
                            self.error_label.config(
                                text=f"❌ Incorrect PIN ({3 - users[current_user_ind]['wrong_tries']} tries left)",
                                foreground=DANGER_COLOR)
                            self.pin = ""
                            for dot in dot_list:
                                dot.config(text='〇', font=('Arial', 30), foreground="blue")
                            self.focus_set()
                        else:
                            usr.blocked = True
                            users[current_user_ind]["blocked"] = True
                            self.error_label.config(text="❌ Card is blocked (Max tries exceeded)", foreground=DANGER_COLOR)
                            break
                except ValueError:
                    pass #print("Continue..")
                break
        if not user_found:
            self.error_label.config(text="❌ User not found", foreground=DANGER_COLOR)
            self.usr.config(state="normal")
            dot_list = []
            self.pin = ""

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage", transition_time_ms=1500)

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(5): self.grid_columnconfigure(j, weight=1)
        self.current_user_label = ttk.Label(self, text="", style='SubTitle.TLabel', foreground=PRIMARY_COLOR)
        self.current_user_label.grid(row=0, column=1, columnspan=3, pady=40, sticky="n")
        self.deposit_button = ttk.Button(self, text="💰 Deposit", style='Primary.TButton',
                                         command=lambda: controller.show_frame("DepositPage", transition_time_ms=3000))
        self.deposit_button.grid(row=2, column=1, pady=20, padx=40, sticky="ew")
        self.transfer_button = ttk.Button(self, text="💸 Transfer", style='Primary.TButton',
                                          command=lambda: controller.show_frame("TransferPage",
                                                                                transition_time_ms=3000))
        self.transfer_button.grid(row=2, column=3, pady=20, padx=40, sticky="ew")

        self.withdraw_button = ttk.Button(self, text="Withdraw", style='Primary.TButton',
                                          command=lambda: controller.show_frame("WithdrawPage",
                                                                                transition_time_ms=3000))
        self.withdraw_button.grid(row=3, column=1, pady=20, padx=40, sticky="ew")
        self.history_button = ttk.Button(self, text="History", style='Primary.TButton',
                                         command=lambda: controller.show_frame("HistoryPage", transition_time_ms=3000))
        self.history_button.grid(row=3, column=3, pady=20, padx=40, sticky="ew")
        self.logout_button = ttk.Button(self, text="Log Out", style='Secondary.TButton', command=self.logout)
        self.logout_button.grid(row=5, column=1, columnspan=3, pady=60, sticky="n")
    def update_page(self):
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=f"Welcome, {user.username} 👋")
        else:
            self.current_user_label.config(text="Welcome, Guest")
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage", transition_time_ms=1500)
class DepositPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)
        ttk.Label(self, text="Deposit Money", style='SubTitle.TLabel', foreground=SUCCESS_COLOR).grid(row=0, column=0,
                                                                                                      columnspan=4,
                                                                                                      padx=20, pady=30,
                                                                                                      sticky="n")
        self.current_user_label = ttk.Label(self, text="")
        self.current_user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")
        self.update_balance_button = ttk.Button(self, text="Show Balance", command=self.show_balance_func,
                                                style='Primary.TButton')
        self.update_balance_button.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        ttk.Label(self, text="Amount:", font=("Segoe UI", 18, "bold")).grid(row=4, column=0, padx=40, pady=30,
                                                                            sticky="e")
        self.amount = ttk.Entry(self, style='TEntry')
        self.amount.grid(row=4, column=1, columnspan=2, padx=20, pady=30, sticky="ew")
        deposit_button_style = {'style': 'Success.TButton'}
        self.deposit_button = ttk.Button(self, text="Deposit", command=self.deposit_action, **deposit_button_style)
        self.deposit_button.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="ew")
        self.MainMenu_button = ttk.Button(self, text="← Main Menu", command=lambda: controller.show_frame("MainMenu"),
                                          style='Secondary.TButton')
        self.MainMenu_button.grid(row=8, column=0, columnspan=4, pady=50, padx=20, sticky="ew")
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=4, sticky="n")

    def deposit_action(self):
        try:
            amount_val = float(self.amount.get())
            if amount_val <= 0:
                self.result_label.config(text="❌ Please enter a valid amount.", foreground=DANGER_COLOR)
                return
        except ValueError:
            self.result_label.config(text="❌ Invalid amount format.", foreground=DANGER_COLOR)
            return
        from transaction import BankAccount
        BankAccount.deposit_money(self.controller.current_user, amount_val, self.current_user_ind)
        self.amount.delete(0, tk.END)
        self.balance_label.config(text=f"Balance: $******")
        self.result_label.config(text=f"✅ Deposit successful: ${amount_val}", foreground=SUCCESS_COLOR)
        self.controller.current_user = None
        self.after(500, lambda: self.controller.show_frame("LoginPage", transition_time_ms=3000))
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
            self.current_user_label.config(text=f"User: {user.username}")
            self.balance_label.config(text="Balance: $******")
            self.result_label.config(text="")  # Mesajları təmizlə
        else:
            self.current_user_label.config(text="User: Guest")
            self.balance_label.config(text="Balance: $0")
class TransferPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)
        ttk.Label(self, text="Transfer Money", style='SubTitle.TLabel', foreground=PRIMARY_COLOR).grid(row=0, column=0,
                                                                                                       columnspan=4,
                                                                                                       padx=20, pady=30,
                                                                                                       sticky="n")
        self.current_user_label = ttk.Label(self, text="")
        self.current_user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")
        ttk.Button(self, text="Show Balance", command=self.show_balance_func, style='Secondary.TButton').grid(
            row=2, column=1, padx=20, pady=5, sticky="w"
        )
        ttk.Button(self, text="← Main Menu", command=lambda: controller.show_frame("MainMenu"),
                   style='Secondary.TButton').grid(
            row=9, column=0, columnspan=4, pady=50, padx=20, sticky="ew"
        )
        ttk.Label(self, text="Amount:").grid(row=4, column=0, padx=40, pady=20, sticky="e")
        self.trsmoney = ttk.Entry(self, style='TEntry')
        self.trsmoney.grid(row=4, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        ttk.Label(self, text="Receiver:").grid(row=5, column=0, padx=40, pady=20, sticky="e")
        self.recvr_var = tk.StringVar()
        self.recvr_var.trace_add("write", self.check_receiver)
        self.recvr = ttk.Entry(self, textvariable=self.recvr_var, style='TEntry')
        self.recvr.grid(row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        self.receiver_status = ttk.Label(self, text="")
        self.receiver_status.grid(row=6, column=1, columnspan=2, padx=10, sticky="w")
        self.transfer_button = ttk.Button(self, text="Transfer", command=self.transfer_action, style='Primary.TButton')
        self.transfer_button.grid(row=7, column=0, columnspan=4, pady=30, padx=20, sticky="ew")
        self.transfer_button.config(state="disabled")
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=8, column=0, columnspan=4, sticky="n")
    def transfer_action(self):
        from transaction import users
        sender = self.controller.current_user
        receiver_name = self.recvr.get().capitalize()
        try:
            amount = float(self.trsmoney.get())
            if amount <= 0:
                self.result_label.config(text="❌ Invalid amount.", foreground=DANGER_COLOR)
                return
        except ValueError:
            self.result_label.config(text="❌ Invalid amount format.", foreground=DANGER_COLOR)
            return
        sender_ind = None
        receiver_ind = None
        for i, u in enumerate(users):
            if u["name"] == sender.username:
                sender_ind = i
            if u["name"] == receiver_name:
                receiver_ind = i
        if sender_ind is None or receiver_ind is None:
            self.result_label.config(text="❌ User not found!", foreground=DANGER_COLOR)
            return
        result = sender.transfer_money(recvr=receiver_name, trsmoney=amount, ind=sender_ind, reind=receiver_ind)

        if result.startswith("Transfer successful"):
            self.balance_label.config(text=f"Balance: $******")
            self.result_label.config(text=f"✅ {result}", foreground=SUCCESS_COLOR)
        else:
            self.result_label.config(text=f"❌ {result}", foreground=DANGER_COLOR)
        self.trsmoney.delete(0, tk.END)
        self.controller.current_user = None
        self.after(500, lambda: self.controller.show_frame("LoginPage", transition_time_ms=3000))
    def update_page(self):
        user = self.controller.current_user
        self.current_user_label.config(text=f"User: {user.username}")
        self.balance_label.config(text=f"Balance: $******")
        self.result_label.config(text="")
        self.receiver_status.config(text="")
        self.recvr_var.set("")
        self.trsmoney.delete(0, tk.END)
    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")
    def check_receiver(self, *args):
        from transaction import users
        recvr = self.recvr_var.get().capitalize()
        if recvr == "":
            self.receiver_status.config(text="")
            self.transfer_button.config(state="disabled")
            return
        current_username = self.controller.current_user.username
        for u in users:
            if u["name"] == recvr:
                if u["name"] == current_username:
                    self.receiver_status.config(text="✗ Cannot transfer to self", foreground=DANGER_COLOR)
                    self.transfer_button.config(state="disabled")
                    return
                self.receiver_status.config(text="✓ User found", foreground=SUCCESS_COLOR)
                self.transfer_button.config(state="normal")
                return
        self.receiver_status.config(text="✗ User not found", foreground=DANGER_COLOR)
        self.transfer_button.config(state="disabled")
class HistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Transaction History", style='SubTitle.TLabel', foreground=SECONDARY_COLOR).pack(pady=30)
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.list_box = tk.Listbox(list_frame, width=60, height=20, font=("Consolas", 12), bg="white", fg="#333333",
                                   selectbackground=PRIMARY_COLOR, yscrollcommand=scrollbar.set, bd=0, relief="flat")
        scrollbar.config(command=self.list_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_box.pack(side=tk.LEFT, fill="both", expand=True)
        self.back_button = ttk.Button(self, text="← Back to Main Menu",
                                      command=lambda: self.controller.show_frame("MainMenu"), style='Secondary.TButton')
        self.back_button.pack(pady=40)
    def update_page(self):
        self.list_box.delete(0, tk.END)
        if self.controller.current_user and self.controller.current_user.trnsct_list:
            for item in reversed(self.controller.current_user.trnsct_list):
                self.list_box.insert(tk.END, item)
        else:
            self.list_box.insert(tk.END, "No transactions yet.")
class WithdrawPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)

        ttk.Label(self, text="Withdraw Cash", style='SubTitle.TLabel', foreground=DANGER_COLOR).grid(row=0, column=0,
                                                                                                     columnspan=4,
                                                                                                     padx=20, pady=30,
                                                                                                     sticky="n")
        self.user_label = ttk.Label(self, text="")
        self.user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")
        self.update_balance_button = ttk.Button(self, text="Show Balance", command=self.show_balance_func,
                                                style='Secondary.TButton')
        self.update_balance_button.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        ttk.Label(self, text="Amount:").grid(row=4, column=0, padx=40, pady=30, sticky="e")
        self.amount = ttk.Entry(self, style='TEntry')
        self.amount.grid(row=4, column=1, columnspan=2, padx=20, pady=30, sticky="ew")
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=4, sticky="n")
        ttk.Button(self, text="Withdraw", command=self.withdraw_action, style='Danger.TButton').grid(row=5, column=0,
                                                                                                     columnspan=4,
                                                                                                     pady=20, padx=20,
                                                                                                     sticky="ew")
        self.back_button = ttk.Button(self, text="← Main Menu", command=lambda: self.controller.show_frame("MainMenu"),
                                      style='Secondary.TButton')
        self.back_button.grid(row=8, column=0, columnspan=4, pady=50, padx=20, sticky="ew")
    def withdraw_action(self):
        user = self.controller.current_user
        try:
            amount = float(self.amount.get())
            if amount <= 0:
                self.result_label.config(text="❌ Please enter a valid amount.", foreground=DANGER_COLOR)
                return
        except ValueError:
            self.result_label.config(text="❌ Invalid amount format.", foreground=DANGER_COLOR)
            return
        user_ind = None
        for i, u in enumerate(users):
            if u["name"] == user.username:
                user_ind = i
                break
        result = user.withdraw_money(amount, user_ind)
        if result.startswith("Withdraw successful"):
            self.balance_label.config(text=f"Balance: $******")
            self.result_label.config(text=f"✅ {result}", foreground=SUCCESS_COLOR)
        else:
            self.result_label.config(text=f"❌ {result}", foreground=DANGER_COLOR)
        self.amount.delete(0, tk.END)
        self.controller.current_user = None
        self.after(500, lambda: self.controller.show_frame("LoginPage", transition_time_ms=3000))
    def show_balance_func(self):
        user = self.controller.current_user
        self.balance_label.config(text=f"Balance: ${user.balance}")
    def update_page(self):
        user = self.controller.current_user
        if user:
            from transaction import users
            user_ind = None
            for i, u in enumerate(users):
                if u["name"] == user.username:
                    user_ind = i
                    break
            if user_ind is not None:
                self.user_label.config(text=f"User: {user.username}")
                self.balance_label.config(text="Balance: $******")
                self.result_label.config(text="")
            else:
                self.user_label.config(text="User: N/A")
                self.balance_label.config(text="Balance: $0")
app = App()
app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
app.title('Modern ATM Interface')
app.mainloop()