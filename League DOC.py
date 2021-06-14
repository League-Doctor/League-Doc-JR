import tkinter as tk
import os
from functools import partial
def buttonPressed(button):
     tk.Label(text = "app ran = "+button).grid(row = 1,column =1)
def getApps():
     apps = []
     files = os.listdir()
     for file in files:
          if str(file) != "League DOC.py":
               apps.append(str(file))
     return apps
window = tk.Tk()
apps = getApps()
label = tk.Label(text="Apps")
label.grid(row=0,column=0)
counter = 1
for app in getApps():
     app = str(app)
     buttonWithArg = partial(buttonPressed,app)
     button = tk.Button(
          text= app,
          width = 20,
          height = 3,
          bg = "black",
          fg = "white",
          command = buttonWithArg
    ).grid(row = counter,  column = 0)
     counter+=1
window.mainloop()
