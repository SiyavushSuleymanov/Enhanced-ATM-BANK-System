def login_user(entered_username, users, entered_pin):
    wrong_pin_counter=0
    for u in users:
        if u["name"]==entered_username.capitalize():
            while wrong_pin_counter<3:
                if u["pin"]==entered_pin:
                    print(f"Welcome to your Bank Account. Your current balance is {u["balance"]}")
                else:
                    wrong_pin_counter+=1
            print("Your card is blocked!!!")
        else:
            print("User doesn't exist")
entered_username=input("Enter the username: ")
entered_pin=int(input("Enter the pin: "))
login_user()