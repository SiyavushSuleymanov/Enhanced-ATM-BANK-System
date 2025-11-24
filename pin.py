from tkinter import *

pin_len = 4

def pressed(event):
    global pin
    if event.keysym.isdigit():
        pin += event.keysym
        upgrade()
        if upgrade() == 1:
            pin = int(pin[:4]) #OUR ENTERED 4-digit PIN (result)
            print(pin)
    elif event.keysym == "BackSpace":
        delete()
        pin = pin[:-1]

def upgrade():
    if len(pin) <= pin_len:
        dots[len(pin)-1].config(text='◉', font=("Arial", 30))
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
