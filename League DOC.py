import tkinter as tk
import importlib
import os
import sys
from functools import partial


def button_pressed(folder_name):
    my_module = importlib.import_module(folder_name)
    my_module.run(tk)


def get_apps():
    apps = []
    files = os.listdir()
    for file in files:
        if "." in file:
            pass
        else:
            apps.append(file)
            path = os.getcwd()+"\\"+file
            sys.path.append(path)
    return apps


window = tk.Tk()
label = tk.Label(text="Apps")
label.grid(row=0, column=0)
counter = 1
for app in get_apps():
    app = str(app)
    button_with_arg = partial(button_pressed, app)
    button = tk.Button(
         text=app,
         width=20,
         height=3,
         bg="black",
         fg="white",
         command=button_with_arg
    ).grid(row=counter,  column=0)
    counter += 1
window.mainloop()
