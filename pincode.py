from tkinter import *

pin_len = 4

def pressed(digit):
    global pin
    if digit.keysym.isdigit() and len(str(pin)) != 4:
        pin += digit.keysym
        upgrade()
        if upgrade() == 1:
            pin = pin[:4] #OUR ENTERED 4-digit PIN - (result)
            print(int(pin))
    elif digit.keysym == "BackSpace":
        if type(pin) == str:
            delete()
            pin = pin[:-1]
        elif type(pin) == int:
            pass

def upgrade():
    if len(pin) <= pin_len:
        dot_list[len(pin)-1].config(text='◉', font=("Arial", 50))
    if len(pin) == pin_len:
        return 1

def delete():
    if len(pin) <= pin_len:
        dot_list[len(pin)-1].config(text='〇', font=("Arial", 30))


window = Tk()
window.title("Enter the PIN")

pin = ""

frm = Frame(window)
frm.pack()

dot_list = []
for _ in range(pin_len):
    dot = Label(frm, text='〇', font=('Arial', 30)) #Dots
    dot.pack(side="left")
    dot_list.append(dot)

digit = window.bind('<Key>', pressed) #Entered digit

window.mainloop()
