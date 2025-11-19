def main_operations():
    operation_name = input("Choose one of them  : Deposit Money, Withdraw Money, Transaction")
    if operation_name.casefold() == "Deposit Money".casefold():
        deposit_money(balance)
    elif operation_name.casefold() == "Withdraw Money".casefold():
        withdraw_money(balance)


def deposit_money(balance):
    amount = float(input("Enter the amount of money: "))
    balance += amount
    print(f"Your current balance is {balance} AZN")
    return transaction(balance, f"+ {amount} is operated")


print(deposit_money(2500))


def withdraw_money(balance):
    print(f"Your current balance is {balance} AZN")
    withdrawed_money = float(input("Enter money you want to get: "))
    if withdrawed_money > balance:
        return "Your balance is low"
    else:
        print("Operation was done succesfully")
        return transaction(balance, f"-{withdrawed_money} is operated")


def transaction(operation, message):
    return  # file you added.append(operation, message)