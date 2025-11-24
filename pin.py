from tkinter import *

pin_len = 4

def pressed(event):
    global pin
    if event.keysym.isdigit() and len(str(pin)) != 4:
        pin += event.keysym
        upgrade()
        if upgrade() == 1:
            pin = pin[:4] #OUR ENTERED 4-digit PIN (result)
            print(int(pin))
    elif event.keysym == "BackSpace":
        if type(pin) == str:
            delete()
            pin = pin[:-1]
        elif type(pin) == int:
            pass

def upgrade():
    if len(pin) <= pin_len:
        dots[len(pin)-1].config(text='◉', font=("Arial", 50))
    if len(pin) == pin_len:
        return 1

def delete():
    if len(pin) <= pin_len:
        dots[len(pin)-1].config(text='〇', font=("Arial", 30))


window = Tk()
window.title("Enter the PIN")

pin = ""

dots = []
for _ in range(pin_len):
    dot = Label(text='〇', font=('Arial', 30))
    dot.pack(side="left")
    dots.append(dot)

event = window.bind('<Key>', pressed)

window.mainloop()
