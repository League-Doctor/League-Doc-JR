import applicationManagement as Am
from win32api import GetSystemMetrics
from tkinter import *
import tkinter as tk
import importlib


class GUI:
    def __init__(self, root):
        # window resolution
        self.width = 0
        self.height = 0

        # storage for app buttons
        self.app_buttons = []
        self.app_button_frames = []

        # root window config
        self.root = root
        self.root.geometry(self.get_start_window_size())
        self.root.title('League Doc')
        self.root.configure(bg="DarkGray")

        # packed frame
        self.centered_frame = Frame(self.root, width=self.width, height=self.height)
        self.centered_frame.place(in_=self.root, anchor="c", relx=.5, rely=.5)

        # app frame
        self.running_app_frame = self.create_running_app_frame()

        # app buttons
        self.apps_list_frame = Frame(self.centered_frame)
        self.app_label_frame = Frame(self.apps_list_frame, width=(int(self.width / 5)), height=int(self.height / 12))
        self.app_label = Label(self.app_label_frame, text="Apps", bg='LightGray')
        self.app_label_frame.propagate(False)
        self.app_label_frame.grid(row=0, column=0)
        self.app_label.pack(expand=True, fill=BOTH)

    def create_running_app_frame(self):
        canvas_frame = Frame(self.centered_frame, width=int(self.width - (self.width / 5)), height=int(self.height))
        canvas = Canvas(canvas_frame)
        running_app_frame = Frame(canvas)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill='y')
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=running_app_frame, anchor='nw')
        running_app_frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox('all'),
                                                               width=int(self.width - (self.width / 5) - 20),
                                                               height=int(self.height) - 20))
        canvas.configure(scrollregion=(0, 0, int(self.width - (self.width / 5) - 20), int(self.height) - 20))

        # test_label = Label(running_app_frame, text='Click on Home Please')
        # test_label.grid(row=0, column=1)
        canvas_frame.grid_propagate(0)
        canvas_frame.grid(row=0, column=1)
        return running_app_frame

    def refresh_favorites(self, fav_apps):
        for x in range(6):
            self.app_buttons[x].configure(text=fav_apps[x][3:])

    def show_app_buttons(self):
        current_row = 1
        Am.get_apps()
        for app in Am.get_favorite_apps():
            app = str(app)[3:]
            size_frame = Frame(self.apps_list_frame, width=int(self.width / 5),
                               height=int((self.height - (self.height / 12)) / 6))
            size_frame.propagate(False)
            button = Button(
                size_frame,
                text=app,
                bg="black",
                fg="white",
                command=lambda text=app: self.run_applications(text)
            )
            self.app_buttons.append(button)
            self.app_button_frames.append(size_frame)
            button.pack(expand=True, fill=BOTH)
            size_frame.grid(row=current_row, column=0)
            current_row += 1
        self.apps_list_frame.grid(row=0, column=0)

    # imports the applications code from its file and executes it
    def run_applications(self, folder_name):
        if folder_name != "":
            my_module = importlib.import_module(folder_name)
            if folder_name =="Home":
                my_module.run(self)
            else:
                my_module.run(self)

    def get_start_window_size(self):
        w_res = GetSystemMetrics(0)
        h_res = GetSystemMetrics(1)

        self.height = int(h_res / 1.5)
        self.width = int((w_res * self.height) / h_res)

        return f'{self.width}x{self.height}'

    def set_scroll_region_size(self, width, height):
        canvas = self.get_parent_widget(self.running_app_frame)
        canvas.configure(scrollregion=(0, 0, width, height))

    @staticmethod
    def get_child_widget(widget):
        widget_name = widget.winfo_child()
        child = Widget._nametowidget(widget, name=widget_name)
        return child

    @staticmethod
    def get_parent_widget(widget):
        widget_name = widget.winfo_parent()
        parent = Widget._nametowidget(widget, name=widget_name)
        return parent
