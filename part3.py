import tkinter as tk #called tkinter library as ts (because of writing in easy way)
from part1 import transl, lang_changer #call this functions from first file

def current_button_refresher():
    label_.config(text=transl("welcome"))  #welcome is shown as label, and when we change language, welcome must be change too
    language_button.config(text=transl("language"))  #language button will change when language changes

def all_button_refresher(lang): #we define this fucntion for all buttons in screen, and also change for label and language button
    lang_changer(lang)
    current_button_refresher()

root=tk.Tk()
root.title("Language Changer Menu")
label_=tk.Label(root, text=transl("welcome"), font=("Arial",25))
label_.pack(pady=25)
language_button=tk.Button(text=transl("language"), command=lambda: all_button_refresher("az"))
language_button.pack()

tk.Button(root, text="AZ", command=lambda: all_button_refresher("az")).pack(side="left", pady=5)
tk.Button(root, text="EN", command=lambda: all_button_refresher("en")).pack(side="left", pady=5)
tk.Button(root, text="RU", command=lambda: all_button_refresher("ru")).pack(side="left", pady=5)

root.mainloop()
