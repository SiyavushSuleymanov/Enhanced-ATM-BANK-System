def login_user(entered_username,entered_pin):
    from users import users
    for u in users:
        if u["name"]==entered_username.capitalize():
            wrong_pin_counter=0
            while wrong_pin_counter<3:
                if u["pin"]==entered_pin:
                    print(f"Welcome to your Bank Account. Your current balance is {u["balance"]}")
                    break
                else:
                    wrong_pin_counter+=1
            print("Your card is blocked!!!")
            break
        else:
            print("User doesn't exist")
entered_username=input("Enter the username: ")
entered_pin=int(input("Enter the pin: "))
login_user(entered_username,entered_pin)


def login_user(self):
    from transaction import users
    usr = self.usr.get().capitalize()
    pin = int(self.entered_pin.get())
    for current_user_ind in range(len(users)):

        if usr == users[current_user_ind]["name"]:
            usr = BankAccount(users[current_user_ind]["name"], users[current_user_ind]["pin"],
                              users[current_user_ind]["balance"], users[current_user_ind]["transactions"])
            self.current_user_ind = current_user_ind
            if pin == users[current_user_ind]["pin"]:
                current_user_ind["wrong_tries"] = 0
                self.controller.current_user = usr
                self.controller.show_frame("MainMenu")
            else:
                current_user_ind["wrong_ties"] += 1
                if current_user_ind["wrong_tries"] < 2:
                    passwd_error = tk.Label(self, text="Incorrect PIN", fg="red")
                    passwd_error.grid(row=5, column=7, columnspan=2, pady=10)
                else:
                    passwd_error = tk.Label(self, text="Card is blocked", fg="red")
                    passwd_error.grid(row=5, column=7, columnspan=2, pady=10)
                    break