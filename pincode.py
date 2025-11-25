from tkinter import *

pin_len = 4 #The length of the PIN

def pressed(ent_digit):
    global pin
    if ent_digit.keysym.isdigit() and len(str(pin)) != 4:
        pin += ent_digit.keysym
        upgrade()
        if upgrade() == 1:
            pin = pin[:4] #OUR ENTERED 4-digit PIN - (result)
            print(int(pin))
    elif ent_digit.keysym == "BackSpace":
        if type(pin) == str:
            delete()
            pin = pin[:-1]
        elif type(pin) == int:
            pass

def upgrade(): #Upgrades dot list
    if len(pin) <= pin_len:
        fdot_list[len(pin)-1].config(text='◉', font=("Arial", 50))
    if len(pin) == pin_len:
        return 1

def delete(): #Deletes dot list
    if len(pin) <= pin_len:
        fdot_list[len(pin)-1].config(text='〇', font=("Arial", 30))


window = Tk()
window.title("Enter the PIN")
frm = Frame(window) #Frame to make dots be together
frm.pack()
pin = "" #Current (entered) PIN

fdot_list = [] #List where dots will be added
for _ in range(pin_len):
    dot = Label(frm, text='〇', font=('Arial', 30)) #Dots
    dot.pack(side="left")
    fdot_list.append(dot)

ent_digit = window.bind('<Key>', pressed) #Entered digit

window.mainloop()
