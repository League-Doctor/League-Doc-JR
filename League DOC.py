import tkinter as tk
import importlib
import os
import sys
from functools import partial
def buttonPressed(button):
     print(sys.path)
     mymodule = importlib.import_module(button)
     mymodule.run(tk)
def getApps():
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
