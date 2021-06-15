from tkinter import *
from functools import partial
import applicationManagement as Am


root = Tk()
app_label = Label(text="Apps")
app_label.grid(row=0, column=0)
counter = 1
for app in Am.get_apps():
    app = str(app)[3:]
    button_with_arg = partial(Am.run_applications, app)
    button = Button(
         text=app,
         width=20,
         height=3,
         bg="black",
         fg="white",
         command=button_with_arg
    ).grid(row=counter,  column=0)
    counter += 1
root.mainloop()
