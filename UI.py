import datetime
import pygame
import webbrowser
import tkinter as tk
from tkinter import Frame, ttk
from PIL import Image, ImageTk
from transaction import BankAccount

""" Language dictionary for multilingual support 
    There are three languages supported: English (ENG), Russian (RUS), Azerbaijani (AZE)
    All buttons, labels, and messages are defined here for easy access and modification."""

LANGUAGES = {
    "ENG": {
        "username": "Username",
        "pin": "PIN",
        "register": "Register",
        "user_not_found": "User not found",
        "card_blocked": "Card is blocked",
        "enter_pin": "Enter 4-digit PIN",
        "incorrect_pin": "Incorrect PIN ({tries} tries left)",
        "max_tries_blocked": "Card is blocked (Max tries exceeded)",
        "welcome": "Welcome, {username} 👋",
        "deposit": "Deposit",
        "withdraw": "Withdraw",
        "transfer": "Transfer",
        "history": "History",
        "logout": "Log Out",
        "amount": "Amount",
        "receiver": "Receiver",
        "show_balance": "Show Balance",
        "main_menu": "Main Menu",
        "deposit_success": "Deposit successful",
        "invalid_amount": "Please enter a valid amount.",
        "invalid_amount_format": "Invalid amount format.",
        "withdraw_success": "Withdraw successful",
        "transfer_success": "Transfer successful",
        "transfer_invalid": "Invalid transfer",
        "cannot_transfer_self": "Cannot transfer to self",
        "no_transactions": "No transactions yet.",
        "not sufficient funds": "Not sufficient funds"
    },
    "RUS": {
        "username": "Имя пользователя",
        "pin": "ПИН",
        "register": "Регистрация",
        "user_not_found": "Пользователь не найден",
        "card_blocked": "Карта заблокирована",
        "enter_pin": "Введите 4-значный ПИН",
        "incorrect_pin": "Неверный ПИН ({tries} попытки осталось)",
        "max_tries_blocked": "Карта заблокирована (Превышено число попыток)",
        "welcome": "Добро пожаловать, {username} 👋",
        "deposit": "Внести",
        "withdraw": "Снять",
        "transfer": "Перевести",
        "history": "История",
        "logout": "Выйти",
        "amount": "Сумма",
        "receiver": "Получатель",
        "show_balance": "Показать баланс",
        "main_menu": "Главное меню",
        "deposit_success": "Внесение успешно",
        "invalid_amount": "Пожалуйста, введите корректную сумму.",
        "invalid_amount_format": "Неверный формат суммы.",
        "withdraw_success": "Снятие успешно",
        "transfer_success": "Перевод успешно",
        "transfer_invalid": "Неверный перевод",
        "cannot_transfer_self": "Нельзя перевести самому себе",
        "no_transactions": "Нет операций.",
        "not sufficient funds": "недостаточно средств"
    },
    "AZE": {
        "username": "İstifadəçi adı",
        "pin": "PIN",
        "register": "Qeydiyyat",
        "user_not_found": "İstifadəçi tapılmadı",
        "card_blocked": "Kart bloklanıb",
        "enter_pin": "4 rəqəmli PIN daxil edin",
        "incorrect_pin": "Səhv PIN ({tries} cəhd qalıb)",
        "max_tries_blocked": "Kart bloklanıb (Maksimum cəhd keçdi)",
        "welcome": "Xoş gəlmisiniz, {username} 👋",
        "deposit": "Əmanət",
        "withdraw": "Çıxarış",
        "transfer": "Köçürmə",
        "history": "Tarixçə",
        "logout": "Çıxış",
        "amount": "Məbləğ",
        "receiver": "Alıcı",
        "show_balance": "Balansı göstər",
        "main_menu": "Əsas menyu",
        "deposit_success": "Əmanət uğurla əlavə edildi",
        "invalid_amount": "Zəhmət olmasa düzgün məbləğ daxil edin.",
        "invalid_amount_format": "Məbləğ formatı düzgün deyil.",
        "withdraw_success": "Çıxarış uğurla edildi",
        "transfer_success": "Köçürmə uğurla edildi",
        "transfer_invalid": "Yanlış köçürmə",
        "cannot_transfer_self": "Özünüzə köçürə bilməzsiniz",
        "no_transactions": "Hələ əməliyyat yoxdur.",
        "not sufficient funds": "Yetersiz balans"
    }
}

PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#6c757d"
SUCCESS_COLOR = "#28a745"
DANGER_COLOR = "#dc3545"
BACKGROUND_COLOR = "#f7f7f7"
FOREGROUND_COLOR = "#333333"

MAIN_FONT = ("Jost", 20, "bold")
TITLE_FONT = ("Jost", 30, "bold")
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

pygame.mixer.init()


def play_ambiance():
    ambiance = pygame.mixer.Sound("sounds/ambiance.wav")
    ambiance.set_volume(0.25)
    ambiance.play(loops=-1)


def play_click():
    pin_sound = pygame.mixer.Sound("sounds/pinsound.mp3")
    pin_sound.set_volume(1)
    pin_sound.play()


def play_success():
    pygame.mixer.Sound("sounds/success.mp3").play()


def play_withdraw():
    withdraw_sound = pygame.mixer.Sound("sounds/withdraw.mp3")
    withdraw_sound.set_volume(1)
    withdraw_sound.play()


def play_error():
    pygame.mixer.Sound("sounds/error-snd.mp3").play()


class App(tk.Tk):
    """This class called App is the main application window that manages different pages and global settings.
       You can access labels, buttons, and other widgets from different pages through this class.
       """

    def __init__(self):
        """init method initializes the main application window, sets up styles, and creates frames for different pages."""
        tk.Tk.__init__(self)
        """Initialize the main application window, set up styles, and create frames for different pages."""
        self.current_user = None
        self.language = "ENG"
        self.frames = {}
        """Firstly, there is no any current user logged in, and default language is English (ENG)
           self.frame{} is frame that holds all frames including different pages of the application."""
        play_ambiance()
        """Start playing ambiance sound that is declared in the below part of the code in a loop."""
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        """ttk.Sty;e is used for styling the widgets in the application.
            Using 'clam' theme for better appearance and customization."""
        self.style.configure('TFrame', background="white")
        """Setting default background color for all frames to white."""
        self.style.configure('TLabel', background="white", font=MAIN_FONT, foreground=FOREGROUND_COLOR)
        """Setting default style for all labels including background color, font(special font name), and foreground color(FOREGROUND_COLOR variable defined above)"""
        self.style.configure('Title.TLabel', font=TITLE_FONT, foreground=PRIMARY_COLOR)
        """Setting specific style for title labels with larger font size and primary color.(primary color variable defined above)"""
        self.style.configure('SubTitle.TLabel', font=("Segoe UI", 20, "bold"), foreground=FOREGROUND_COLOR)
        """Setting specific style for subtitle labels with slightly smaller font size and foreground color(FOREGROUND_COLOR variable defined above)"""""
        self.style.configure('Primary.TButton', font=("Segoe UI", 16, "bold"), background=PRIMARY_COLOR,
                             foreground="white", borderwidth=0, relief="flat", padding=15)
        self.style.map('Primary.TButton', background=[('active', '#0056b3')])
        """Setting specific style for primary buttons with font, background color(PRIMARY_COLOR variable defined above), foreground color(white), border width(0), flat relief, and padding(15)
           Border width 0 and flat relief gives a modern look to the buttons.
           Padding of 15px makes buttons larger and easier to click.
           The map method is used to change the background color when the button is active (clicked or hovered over)."""
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
        """The rest buttons and entry fields are also styled similarly with appropriate colors and fonts."""
        try:
            image_path = "bg.png"
            original_image = Image.open(image_path)
            resized_image = original_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self, image=self.bg_image)
            background_label.image = self.bg_image
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            container = Frame(self)
            """Loading and setting a background image that is in your computer folder for the application window.
               It makes the application visually appealing for your devices.
               Then we stores the image in self.bg_image to prevent it from being garbage collected.
               When the image is not stored, it may not display correctly.Beccause, if image is not stored, Python's garbage collector may remove it from memory, leading to display issues."""
        except FileNotFoundError:
            print(f"WARNING: Image {image_path} not found. Using default background.")
            container = Frame(self, bg=BACKGROUND_COLOR)
        except Exception as e:
            print(f"ERROR: A problem occurred while loading the image: {e}")
            container = Frame(self, bg=BACKGROUND_COLOR)
            """If the image file is not found or any other error occurs during loading, it prints a warning or error message and uses a default background color instead."""
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        """Creating a container frame that holds all other frames (pages) of the application.
           The container is packed to fill the entire window with some padding.
           Grid configuration is set to allow frames to expand and fill the container."""
        for F in (LoginPage, MainMenu, DepositPage, TransferPage, HistoryPage, WithdrawPage, LoadingPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("LoginPage")
        """F is a class representing each page of the application.
           F will be one of the classes defined below like LoginPage, MainMenu, DepositPage, etc.
           page_name gets the name of the class as a string.(__name__ is a special attribute that holds the name of the class.)
           frame creates an instance of the page class, passing the container as the parent and the main application (self) as the controller
           Each frame is stored in the frames dictionary with its name as the key.
           Each frame is placed in the grid of the container, all stacked on top of each other.(we declare row=0, column=0 for all frames, so they overlap each other)
           sticky='nsew' makes the frames expand to fill the entire container. (nsew- North, South, East, West)
           Finally, the show_frame method is called to display the LoginPage(because, it is a inital page that have to be shown firstly) when the application starts."""

    def set_language(self, lang_code):
        """Define application's lanugage as lang_code parameter that is passed to this method.
           It updates the language for all frames that have an update_labels method.
           Then it calls the update_labels method for each frame to refresh the displayed text according to the selected language.
           hassatr is a function that checks if an object has a specific attribute or method.(in our code, it checks if frame has update_labels method)
           Finally, it updates the labels on each frame to reflect the new language setting."""
        self.language = lang_code
        for frame in self.frames.values():
            if hasattr(frame, "update_labels"):
                frame.update_labels()

    def show_frame(self, page_name, transition_time_ms=0):
        """This method is responsible for displaying a specific frame (page) in the application.
           page_name is the name of the frame to be displayed.
           transition_time_ms is an optional parameter that specifies a delay before showing the frame (in milliseconds).
           If transition_time_ms is greater than 0, it uses the after method to schedule the frame change after the specified delay.
           If no delay is specified, it immediately raises the specified frame to the front using tkraise().
           If the frame has an update_page method, it calls that method to refresh any dynamic content on the page before displaying it."""
        self.current_frame_name = page_name
        frame = self.frames[page_name]
        if hasattr(frame, "update_page"):
            frame.update_page()
        frame.tkraise()


class LoadingPage(ttk.Frame):
    """ You create a new class called LoadingPage that inherits from ttk.Frame.
        This class represents a loading page that displays a progress bar and messages while processing a transaction.
        """

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
    """This class represents the login page of the ATM application."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.lang_var = tk.StringVar(value="ENG")  # default
        """parent is the parent widget (container) that holds this frame.
           controller is the main application instance that manages different pages and global settings.
           self.lang_var is a StringVar that holds the selected language code, defaulting to "ENG" (English)."""

        lang_choice = ttk.Combobox(
            self,
            textvariable=self.lang_var,
            values=["ENG", "RUS", "AZE"],
            state="readonly",
            width=5,
            font=("Segoe UI", 12, "bold")
        )
        lang_choice.grid(row=7, column=7, pady=160, sticky="en")
        lang_choice.bind("<<ComboboxSelected>>", self.change_language)
        """Creating a Combobox widget for language selection.
           The Combobox is populated with language codes ("ENG", "RUS", "AZE").
           It is placed in the grid at row 7, column 7 with 160px padding."""
        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(10): self.grid_columnconfigure(j, weight=1)

        self.title_label = ttk.Label(self, text="UFAZ BANK 💳", style='Title.TLabel')
        self.title_label.grid(row=1, column=1, columnspan=8, pady=50, sticky="n")
        """Creating a title label for the login page with the text "UFAZ BANK 💳
           It uses the 'Title.TLabel' style defined in the App class for styling
           """

        self.username_label = ttk.Label(self, text="Username :", font=("Segoe UI", 20, "bold"))
        self.username_label.grid(row=3, column=2, columnspan=2, sticky="e", padx=10, pady=20)

        self.usir = ttk.Entry(self, style='TEntry', font=("Helvetica", 16, "bold"))
        self.usir.focus_set()
        self.usir.grid(row=3, column=5, columnspan=3, sticky="w", padx=10, pady=20)
        self.usir.bind("<Return>", self.enterr)
        """Creating a label for the username input field with the text "Username 
           It is placed in the grid at row 3, column 2 with appropriate padding.
           Creating an Entry widget for username input.
           It uses the 'TEntry' style defined in the App class for styling"""

        self.pin_label = ttk.Label(self, text="PIN :", font=("Segoe UI", 18, "bold"))
        self.pin_label.grid(row=6, column=1, columnspan=4, sticky="e", padx=7, pady=20)
        """Creating a label for the PIN input field with the text "PIN
           It is placed in the grid at row 6, column 1 with appropriate padding."""

        # 5

        self.register_button = ttk.Button(self, text="Register", command=self.open_register_page,
                                          style='Secondary.TButton')
        self.register_button.grid(row=7, column=3, columnspan=4, pady=40, sticky="ew")
        """Creating a button for registration with the text "Register
           It uses the 'Secondary.TButton' style defined in the App class for styling.
           When clicked, it calls the open_register_page method to open the registration page in a web browser."""

        self.error_label = ttk.Label(self, text="", foreground=DANGER_COLOR, background="white")
        self.error_label.grid(row=7, column=2, columnspan=6, pady=5, sticky="n")
        """Creating a label for displaying error messages.
           Initially, it is empty and will be updated with error messages as needed.
           It uses the DANGER_COLOR defined above for the foreground color.(That is declared as red color above part of the code)"""

        self.pin_len = 4
        self.pin = ""
        self.dot_list = []
        frm = ttk.Frame(self)
        frm.grid(row=6, column=4, columnspan=3, padx=10, pady=20)
        for _ in range(self.pin_len):
            dot = ttk.Label(frm, text='〇', font=('Arial', 30), foreground="blue")
            dot.pack(side="left")
            self.dot_list.append(dot)
        """Creating a frame to hold the PIN input dots.
           The frame is placed in the grid at row 6, column 4 with appropriate padding
           This loop creates 4 dot labels (〇) to represent the PIN input.
           Each dot is styled with a blue color and a large font size when the user types their PIN."""

        self.focus_set()
        self.bind('<Key>', self.pressed)
        """Binding the key press event to the pressed method.
           This allows the user to enter their PIN using the keyboard."""

    def enterr(self, k):
        self.error_label.config(text="")
        usr_input = self.usir.get()
        self.usr = BankAccount.get_user(usr_input)
        if not self.usr:
            self.error_label.config(text="❌ User not found", foreground=DANGER_COLOR)
            play_error()
            self.usir.config(state="normal")
            self.pin = ""
            return #212
        if self.usir['state'] == 'normal':
            self.usir.config(state='disabled')
        elif self.usir['state'] == 'disabled':
            self.usir.config(state='normal')
        self.usr.wrong_tries = 0
        self.pin = ""
        for dot in self.dot_list:
            dot.config(text='〇', font=('Arial', 30), foreground="blue")
        self.focus_set()
        """First, it clears any existing error messages by setting the text of the error_label to an empty string.
           Then, it retrieves the username entered by the user in the usr Entry widget.
           It calls the get_user method of the BankAccount class to check if the user exists in
           the database. If the user is not found, it updates the error_label with a "User not found" message,
           plays an error sound, resets the usr Entry widget to normal state, clears the PIN input,
           and returns from the method.
           If the user is found, it checks the state of the usr Entry widget. If it is in 'normal' state, it disables it to prevent further input.
           If it is already disabled, it enables it.
           It resets the wrong_tries attribute of the user to 0.
           It clears the PIN input and resets the dot labels to their initial state (〇).
           Finally, it sets the focus back to the LoginPage frame to allow further input."""

    def change_language(self, event=None):
        selected_lang = self.lang_var.get()
        self.controller.set_language(selected_lang)
        self.update_labels()
        """ This method is called when the user selects a different language from the Combobox.
            It retrieves the selected language code from the lang_var StringVar.
            It calls the set_language method of the controller (main application) to update the language for all frames.
            Finally, it calls the update_labels method to refresh the labels on the LoginPage frame to reflect the new language setting."""

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.username_label.config(text=f"{lang['username']} :")
        self.pin_label.config(text=f"{lang['pin']} :")
        self.register_button.config(text=lang['register'])
        """This function updates the text of various labels and buttons on the LoginPage frame based on the selected language.
           It retrieves the appropriate language dictionary from the LANGUAGES dictionary using the current language setting from the controller.
           It then updates the text of the username_label, pin_label, and register_button to reflect the selected language."""

    def pressed(self, ent_digit):
        if self.usr.blocked == False:
            play_click()
            self.error_label.config(text="")
            if ent_digit.keysym.isdigit() and len(self.pin) <= self.pin_len:
                self.pin += ent_digit.keysym
                self.upgrade()
                if self.upgrade() == 1:
                    self.after(5, self.login_user)

            elif ent_digit.keysym == "BackSpace":
                if len(self.pin) > 0:
                    self.delete()
                    self.pin = self.pin[:-1]
                elif type(self.pin) == int:
                    pass
        else:
            self.error_label.config(text="❌ Card is blocked", foreground=DANGER_COLOR)
            play_error()

    def upgrade(self):
        try:
            if len(self.pin) <= self.pin_len:
                self.dot_list[len(self.pin) - 1].config(text='◉', font=("Arial", 30), foreground="blue")
            if len(self.pin) == self.pin_len:
                self.dot_list[-1].config(text='◉', font=("Arial", 30), foreground="blue")
                return 1
        except IndexError:
            pass

    def delete(self):
        if len(self.pin) <= self.pin_len:
            self.dot_list[len(self.pin) - 1].config(text='〇', font=("Arial", 30), foreground="blue")

    def open_register_page(self):
        url = "http://ufaz-final-project-registration-page-atm.vercel.app/"
        webbrowser.open(url)

    """This method opens the registration page in the default web browser.
       It uses the webbrowser module to open the specified URL."""

    def login_user(self, k=0):
        self.usir.config(state="active")

        usr_input = self.usir.get()
        self.error_label.config(text="")
        self.usr = BankAccount.get_user(usr_input)
        if not self.usr:
            self.error_label.config(text="❌ User not found", foreground=DANGER_COLOR)
            play_error()
            self.usir.config(state="normal")
            self.pin = ""
            return

        if self.usr.blocked:
            self.error_label.config(text="❌ Card is blocked", foreground=DANGER_COLOR)
            play_error()
            return

        if len(self.pin) != 4:
            self.error_label.config(text="❗ Enter 4-digit PIN", foreground=DANGER_COLOR)
            play_error()
            return
        """This method attempts to log in the user based on the entered username and PIN.
       It first retrieves the username from the usr Entry widget and clears any existing error messages.
       It then checks if the user exists in the database using the get_user method of the BankAccount class.
       If the user is not found, it updates the error_label with a "User not found" message, plays an error sound, resets the usr Entry widget to normal state, clears the PIN input, and returns from the method.
       If the user is found but the card is blocked, it updates the error_label with a "Card is blocked" message, plays an error sound, and returns from the method.
       If the entered PIN length is not equal to 4, it updates the error_label with a "Enter 4-digit PIN" message, plays an error sound, and returns from the method."""

        try:
            if self.pin == str(self.usr.pin):
                self.usr.wrong_tries = 0
                self.pin = ""
                for dot in self.dot_list:
                    dot.config(text='〇', font=('Arial', 30), foreground="blue")
                self.focus_set()
                self.usr.update_db()
                self.controller.current_user = self.usr
                self.usir.delete(0, tk.END)
                self.controller.show_frame("LoadingPage")
                self.controller.after(1500, lambda: self.controller.show_frame("MainMenu"))
            else:
                self.usr.wrong_tries += 1
                if self.usr.wrong_tries < 3:
                    self.usr.update_db()
                    self.error_label.config(
                        text=f"❌ Incorrect PIN ({3 - self.usr.wrong_tries} tries left)",
                        foreground=DANGER_COLOR
                    )
                    play_error()
                    self.pin = ""
                    for dot in self.dot_list:
                        dot.config(text='〇', font=('Arial', 30), foreground="blue")
                    self.focus_set()
                else:
                    self.usr.blocked = True
                    self.usr.update_db()
                    self.error_label.config(text="❌ Card is blocked (Max tries exceeded)", foreground=DANGER_COLOR)
                    play_error()
                    self.pin = ""
                    for dot in self.dot_list:
                        dot.config(text='〇', font=('Arial', 31), foreground="blue")
                    self.focus_set()
        except ValueError:
            pass
        """The method then checks if the entered PIN matches the user's stored PIN.
           If the PIN is correct, it resets the wrong_tries counter, clears the PIN input,
           resets the dot labels, sets the focus back to the LoginPage frame, updates the user
           in the database, sets the current_user in the controller to the logged-in user,
           clears the usr Entry widget, shows the LoadingPage frame, and after a delay of 1500 milliseconds,
           it shows the MainMenu frame.
           If the PIN is incorrect, it increments the wrong_tries counter. If the number of wrong tries is less than 3,
           it updates the user in the database, updates the error_label with an "Incorrect PIN" message showing the remaining tries,
           plays an error sound, clears the PIN input, resets the dot labels, and sets the focus back to the LoginPage frame.
           If the number of wrong tries reaches 3, it blocks the user's card, updates the user in the database,
           updates the error_label with a "Card is blocked message, plays an error sound, clears the PIN input,
           resets the dot labels, and sets the focus back to the LoginPage frame."""

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage", transition_time_ms=1500)

    """This method logs out the current user by setting the current_user attribute of the controller to None."""


class MainMenu(ttk.Frame):
    """This class represents the main menu page of the ATM application.
    It provides options for depositing, transferring, withdrawing money, viewing transaction history, and logging out.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.deposit_icon = ImageTk.PhotoImage(Image.open("deposit.png").resize((32, 32)))
        self.transfer_icon = ImageTk.PhotoImage(Image.open("transfer_money.png").resize((32, 32)))
        self.withdraw_icon = ImageTk.PhotoImage(Image.open("withdraw.png").resize((32, 32)))
        self.history_icon = ImageTk.PhotoImage(Image.open("history.png").resize((32, 32)))

        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(5): self.grid_columnconfigure(j, weight=1)

        self.current_user_label = ttk.Label(
            self, text="", style='SubTitle.TLabel', foreground=PRIMARY_COLOR
        )
        self.current_user_label.grid(row=2, column=1, columnspan=3, pady=40, sticky="n")

        self.deposit_button = ttk.Button(
            self, text="", image=self.deposit_icon, compound="left",
            style='Primary.TButton',
            command=lambda: controller.show_frame("DepositPage", transition_time_ms=3000)
        )
        self.deposit_button.grid(row=3, column=1, pady=20, padx=40, sticky="ew")

        self.transfer_button = ttk.Button(
            self, text="", image=self.transfer_icon, compound="left",
            style='Primary.TButton',
            command=lambda: controller.show_frame("TransferPage", transition_time_ms=3000)
        )
        self.transfer_button.grid(row=3, column=3, pady=20, padx=40, sticky="ew")

        self.withdraw_button = ttk.Button(
            self, text="", image=self.withdraw_icon, compound="left",
            style='Primary.TButton',
            command=lambda: controller.show_frame("WithdrawPage", transition_time_ms=3000)
        )
        self.withdraw_button.grid(row=4, column=1, pady=20, padx=40, sticky="ew")

        self.history_button = ttk.Button(
            self, text="", image=self.history_icon, compound="left",
            style='Primary.TButton',
            command=lambda: controller.show_frame("HistoryPage", transition_time_ms=3000)
        )
        self.history_button.grid(row=4, column=3, pady=20, padx=40, sticky="ew")

        self.logout_button = ttk.Button(
            self, text="", compound="left",
            style='Secondary.TButton',
            command=self.logout
        )
        self.logout_button.grid(row=5, column=1, columnspan=3, pady=60, sticky="n")
        self.update_labels()

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.deposit_button.config(text=f"   {lang['deposit']}")
        self.transfer_button.config(text=f"   {lang['transfer']}")
        self.withdraw_button.config(text=f"   {lang['withdraw']}")
        self.history_button.config(text=f"   {lang['history']}")
        self.logout_button.config(text=f"   {lang['logout']}")
        """This method updates the text of various buttons and labels on the MainMenu frame based on the selected language.
           It retrieves the appropriate language dictionary from the LANGUAGES dictionary using the current language setting from the controller.
           It then updates the text of the deposit_button, transfer_button, withdraw_button, history_button, and logout_button to reflect the selected language.
           It also updates the current_user_label to welcome the current user by their username."""

        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=lang['welcome'].format(username=user.username))
        else:
            self.current_user_label.config(text=lang['welcome'].format(username="Guest"))

    def update_page(self):

        lang = LANGUAGES[self.controller.language]
        user = self.controller.current_user
        if user:
            self.current_user_label.config(text=lang['welcome'].format(username=user.username))
        else:
            self.current_user_label.config(text=lang['welcome'].format(username="Guest"))

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage", transition_time_ms=1500)

    """This method logs out the current user by setting the current_user attribute of the controller to None.
       It then shows the LoginPage frame after a delay of 1500 milliseconds."""


class DepositPage(ttk.Frame):
    """This class represents the deposit page of the ATM application.
       It allows users to deposit money into their account and view their current balance."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)

        self.title_label = ttk.Label(self, text="", style='SubTitle.TLabel', foreground=SUCCESS_COLOR)
        self.title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=30, sticky="n")

        self.current_user_label = ttk.Label(self, text="")
        self.current_user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")

        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")

        self.update_balance_button = ttk.Button(self, text="", command=self.show_balance_func, style='Primary.TButton')
        self.update_balance_button.grid(row=2, column=1, padx=20, pady=5, sticky="w")

        self.amount_label = ttk.Label(self, text="", font=("Jost", 18, "bold"))
        self.amount_label.grid(row=4, column=0, padx=40, pady=30, sticky="e")

        self.amount = ttk.Entry(self, style='TEntry')
        self.amount.grid(row=4, column=1, columnspan=2, padx=20, pady=30, sticky="ew")

        self.deposit_button = ttk.Button(self, text="", command=self.deposit_action, style='Success.TButton')
        self.deposit_button.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="ew")

        self.MainMenu_button = ttk.Button(self, text="", command=lambda: controller.show_frame("MainMenu"),
                                          style='Secondary.TButton')
        self.MainMenu_button.grid(row=8, column=0, columnspan=4, pady=50, padx=20, sticky="ew")

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=4, sticky="n")

        self.update_labels()
        self.update_page()

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.title_label.config(text=lang['deposit'])
        self.amount_label.config(text=f"{lang['amount']}:")
        self.deposit_button.config(text=lang['deposit'])
        self.update_balance_button.config(text=lang.get('show_balance', 'Show Balance'))
        self.MainMenu_button.config(text=f"← {lang.get('main_menu', 'Main Menu')}")

    def update_page(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        if user:
            self.current_user_label.config(text=f"{lang['welcome'].format(username=user.username)}")
            self.balance_label.config(text=f"{lang['amount']}: ******")
        else:
            self.current_user_label.config(text=f"{lang['welcome'].format(username='Guest')}")
            self.balance_label.config(text=f"{lang['amount']}: 0")
        self.result_label.config(text="")
        self.amount.delete(0, tk.END)

    def deposit_action(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]

        try:
            zeroch = str(self.amount.get())
            amount_val = int(self.amount.get())
            if amount_val <= 0 or zeroch[0] == '0':
                self.result_label.config(text=f"❌ {lang.get('invalid_amount')}", foreground=DANGER_COLOR)
                play_error()
                return
        except ValueError:
            self.result_label.config(text=f"❌ {lang.get('invalid_amount_format')}", foreground=DANGER_COLOR)
            play_error()
            return

        from transaction import BankAccount
        BankAccount.deposit(user, amount_val)
        self.amount.delete(0, tk.END)
        play_success()

        self.controller.show_frame("LoadingPage")
        self.controller.after(1500, lambda: self.controller.show_frame("MainMenu"))

    def show_balance_func(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        if user:
            self.balance_label.config(text=f"{lang.get('amount')}: {user.balance} AZN")
        else:
            self.balance_label.config(text=f"{lang.get('amount')}: 0 AZN")


class WithdrawPage(ttk.Frame):
    """This class represents the withdraw page of the ATM application.
       It allows users to withdraw money from their account and view their current balance.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)

        self.title_label = ttk.Label(self, text="", style='SubTitle.TLabel', foreground=DANGER_COLOR)
        self.title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=30, sticky="n")

        self.user_label = ttk.Label(self, text="")
        self.user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")
        self.show_balance_button = ttk.Button(self, text="", command=self.show_balance_func, style='Secondary.TButton')
        self.show_balance_button.grid(row=2, column=1, padx=20, pady=5, sticky="w")

        self.amount_label = ttk.Label(self, text="")
        self.amount_label.grid(row=4, column=0, padx=40, pady=30, sticky="e")
        self.amount = ttk.Entry(self, style='TEntry')
        self.amount.grid(row=4, column=1, columnspan=2, padx=20, pady=30, sticky="ew")

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=4, sticky="n")

        self.withdraw_button = ttk.Button(self, text="", command=self.withdraw_action, style='Danger.TButton')
        self.withdraw_button.grid(row=5, column=0, columnspan=4, pady=20, padx=20, sticky="ew")

        self.back_button = ttk.Button(self, text="", command=lambda: controller.show_frame("MainMenu"),
                                      style='Secondary.TButton')
        self.back_button.grid(row=8, column=0, columnspan=4, pady=50, padx=20, sticky="ew")

        self.update_labels()

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.title_label.config(text=lang['withdraw'])
        self.amount_label.config(text=f"{lang['amount']}:")
        self.withdraw_button.config(text=lang['withdraw'])
        self.show_balance_button.config(text=lang['show_balance'])
        self.back_button.config(text=f"← {lang['main_menu']}")
        self.update_page()

    """This method updates the text of various labels and buttons on the WithdrawPage frame based on the selected language.
       It retrieves the appropriate language dictionary from the LANGUAGES dictionary using the current language setting from the controller.
       It then updates the text of the title_label, amount_label, withdraw_button, show_balance_button, and back_button to reflect the selected language.
       Finally, it calls the update_page method to refresh the page content. """

    def update_page(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        if user:
            self.user_label.config(text=f"{lang['welcome'].format(username=user.username)}")
            self.balance_label.config(text=f"{lang['amount']}: ******")
        else:
            self.user_label.config(text=f"{lang['welcome'].format(username='Guest')}")
            self.balance_label.config(text=f"{lang['amount']}: 0")
        self.result_label.config(text="")
        self.amount.delete(0, tk.END)

    def show_balance_func(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        if user:
            self.balance_label.config(text=f"{lang['amount']}: ${user.balance}")

    def withdraw_action(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]

        try:
            zeroch = str(self.amount.get())
            amount = int(self.amount.get())
            if amount <= 0 or zeroch[0] == '0' or amount > user.balance:
                if amount > user.balance:
                    self.result_label.config(text=f"❌ {lang['not sufficient funds']}", foreground=DANGER_COLOR)
                    play_error()
                else:
                    self.result_label.config(text=f"❌ {lang['invalid_amount']}", foreground=DANGER_COLOR)
                    play_error()
                return
        except ValueError:
            self.result_label.config(text=f"❌ {lang['invalid_amount_format']}", foreground=DANGER_COLOR)
            play_error()
            return

        user.withdraw(amount)
        self.amount.delete(0, tk.END)

        play_withdraw()

        play_success()
        self.controller.show_frame("LoadingPage")
        self.controller.after(1500, lambda: self.controller.show_frame("MainMenu"))


class TransferPage(ttk.Frame):
    """This class represents the transfer page of the ATM application.
       It allows users to transfer money to another user's account and view their current balance."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(10): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)

        self.title_label = ttk.Label(self, text="", style='SubTitle.TLabel', foreground=PRIMARY_COLOR)
        self.title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=30, sticky="n")

        self.current_user_label = ttk.Label(self, text="")
        self.current_user_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")
        self.show_balance_button = ttk.Button(self, text="", command=self.show_balance_func, style='Secondary.TButton')
        self.show_balance_button.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        """ Creating a button to show the current balance.
            When clicked, it calls the show_balance_func method to display the user's balance."""

        self.amount_label = ttk.Label(self, text="")
        self.amount_label.grid(row=4, column=0, padx=40, pady=20, sticky="e")
        self.trsmoney = ttk.Entry(self, style='TEntry')
        self.trsmoney.grid(row=4, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        self.receiver_label = ttk.Label(self, text="")
        self.receiver_label.grid(row=5, column=0, padx=40, pady=20, sticky="e")
        self.recvr_var = tk.StringVar()
        self.recvr_var.trace_add("write", self.check_receiver)
        self.recvr = ttk.Entry(self, textvariable=self.recvr_var, style='TEntry')
        self.recvr.grid(row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        self.receiver_status = ttk.Label(self, text="")
        self.receiver_status.grid(row=6, column=1, columnspan=2, padx=10, sticky="w")

        self.transfer_button = ttk.Button(self, text="", command=self.transfer_action, style='Danger.TButton')
        self.transfer_button.grid(row=7, column=0, columnspan=4, pady=30, padx=20, sticky="ew")

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=8, column=0, columnspan=4, sticky="n")

        self.back_button = ttk.Button(self, text="", command=lambda: controller.show_frame("MainMenu"),
                                      style='Secondary.TButton')
        self.back_button.grid(row=9, column=0, columnspan=4, pady=50, padx=20, sticky="ew")

        self.update_labels()

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.title_label.config(text=lang['transfer'])
        self.amount_label.config(text=f"{lang['amount']}:")
        self.receiver_label.config(text=f"{lang['receiver']}:")
        self.transfer_button.config(text=lang['transfer'])
        self.show_balance_button.config(text=lang['show_balance'])
        self.back_button.config(text=f"← {lang['main_menu']}")
        self.update_page()

    def update_page(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]

        if user:
            self.current_user_label.config(text=lang['welcome'].format(username=user.username))
            self.balance_label.config(text=f"{lang['amount']}: ******")
        else:
            self.current_user_label.config(text=lang['welcome'].format(username='Guest'))
            self.balance_label.config(text=f"{lang['amount']}: 0")

        self.result_label.config(text="")
        self.receiver_status.config(text="")
        self.recvr_var.set("")
        self.trsmoney.delete(0, tk.END)
        self.transfer_button.config(command=lambda: None)

    def show_balance_func(self):
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        if user:
            self.balance_label.config(text=f"{lang['amount']}: {user.balance} AZN")

    def check_receiver(self, *args):
        from transaction import BankAccount
        recvr = self.recvr_var.get()
        lang = LANGUAGES[self.controller.language]
        user = self.controller.current_user

        if recvr == "":
            self.receiver_status.config(text="")
            self.transfer_button.config(command=lambda: None, style='Danger.TButton')
            return

        receiver = BankAccount.get_user(recvr)
        current_username = user.username if user else ""

        if not receiver:
            self.receiver_status.config(text=f"✗ {lang['user_not_found']}", foreground=DANGER_COLOR)
            self.transfer_button.config(command=lambda: None, style='Danger.TButton')
        elif receiver.username == current_username:
            self.receiver_status.config(text=f"✗ {lang['cannot_transfer_self']}", foreground=DANGER_COLOR)
            self.transfer_button.config(command=lambda: None, style='Danger.TButton')
        else:
            self.receiver_status.config(text="✓ User found", foreground=SUCCESS_COLOR)
            self.transfer_button.config(state="normal", style='Primary.TButton', command=self.transfer_action)

    def transfer_action(self):
        from transaction import BankAccount
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]
        receiver_name = self.recvr.get()
        receiver = BankAccount.get_user(receiver_name)

        try:
            zeroch = str(self.trsmoney.get())
            amount = float(self.trsmoney.get())
            if amount <= 0 or len(str(amount).split('.')[1]) > 2 or (zeroch[0] == '0' and zeroch[1] != '.') or amount > user.balance:
                if amount < user.balance:
                    self.result_label.config(text=f"❌ {lang['not sufficient funds']}", foreground=DANGER_COLOR)
                    play_error()
                else:
                    self.result_label.config(text=f"❌ {lang['invalid_amount']}", foreground=DANGER_COLOR)
                    play_error()
                return
            else:
                play_success()
                self.controller.show_frame("LoadingPage")
                self.controller.after(1500, lambda: self.controller.show_frame("MainMenu"))
        except ValueError:
            self.result_label.config(text=f"❌ {lang['invalid_amount_format']}", foreground=DANGER_COLOR)
            play_error()
            return

        if not receiver or receiver.username == user.username:
            self.result_label.config(text=f"❌ {lang['transfer_invalid']}", foreground=DANGER_COLOR)
            play_error()
            return

        user.transfer(receiver, amount)


class HistoryPage(ttk.Frame):
    """This class represents the transaction history page of the ATM application.
       It displays a list of past transactions made by the user.
       """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.title_label = ttk.Label(self, text="", style='SubTitle.TLabel', foreground=SECONDARY_COLOR)
        self.title_label.pack(pady=30)

        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.list_box = tk.Listbox(list_frame, width=60, height=20, font=("Consolas", 12),
                                   bg="white", fg="#333333", selectbackground=PRIMARY_COLOR,
                                   yscrollcommand=self.scrollbar.set, bd=0, relief="flat")
        self.scrollbar.config(command=self.list_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_box.pack(side=tk.LEFT, fill="both", expand=True)
        """Creating a frame to hold the Listbox and Scrollbar.
           The frame is packed with padding and set to fill both horizontally and vertically.
           A vertical Scrollbar is created and configured to control the Listbox's vertical scrolling.
           The Listbox is created with specific styling, including font, colors, and dimensions.
           The Scrollbar is packed to the right side of the frame, and the Listbox is packed to the left side, filling the remaining space."""

        self.back_button = ttk.Button(self, text="", command=lambda: self.controller.show_frame("MainMenu"),
                                      style='Secondary.TButton')
        self.back_button.pack(pady=40)

        self.update_labels()

    def update_labels(self):
        lang = LANGUAGES[self.controller.language]
        self.title_label.config(text=lang['history'])
        self.back_button.config(text=f"← {lang['main_menu']}")
        self.update_page()

    def update_page(self):
        self.list_box.delete(0, tk.END)
        user = self.controller.current_user
        lang = LANGUAGES[self.controller.language]

        if user and getattr(user, "transactions", None):
            for item in reversed(user.transactions):
                self.list_box.insert(tk.END, item)
        else:
            self.list_box.insert(tk.END, lang['no_transactions'])


app = App()
app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
app.title('Ufaz Bank')
app.mainloop()