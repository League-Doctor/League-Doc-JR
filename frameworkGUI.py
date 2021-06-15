import applicationManagement as Am
from tkinter import *
from verticalScrolledFrame import VerticalScrolledFrame


class GUI:

    def __init__(self, root):
        self.root = root
        # self.root.geometry('960x540')
        self.root.title('League Doc')
        self.app_label = Label(text="Apps")
        self.app_label.grid(row=0, column=0)
        self.app_frame = Frame(root, width=20, height=30)

    def show_app_buttons(self):
        counter = 1
        for app in Am.get_apps():
            app = str(app)[3:]
            button = Button(
                 self.app_frame,
                 text=app,
                 width=20,
                 height=int(16/len(Am.get_apps())),
                 bg="black",
                 fg="white",
                 command=lambda text=app: Am.run_applications(text)
            )
            button.grid(row=counter, column=0)
            counter += 1
        self.app_frame.grid(row=0, column=0)
