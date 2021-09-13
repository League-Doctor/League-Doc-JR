"""
frameworkGUI

This program initializes and maintains the root window. In this window it places the favourite app buttons, and the
<running app frame> which is where the selected application will run. This class also supports the movement between two
such applications.

@author Joseph Miller
@version September 12, 2021

"""

import applicationManagement as Am
from win32api import GetSystemMetrics
from tkinter import *
import colorScheme as Cs
import importlib

color_scheme = Cs.basic_color_scheme  # access to selected color scheme


class GUI:
    def __init__(self, root):
        # api key: must be updated every 24 hours
        self.api_key = 'RGAPI-d581cce3-cb74-4da7-931f-1c82302477cc'  # Personal API required. Expires after 24hrs

        # window resolution
        self.width = 0
        self.height = 0
        self.default_height = 0

        # storage for app buttons
        self.app_buttons = []
        self.app_button_frames = []

        # root window config
        self.root = root
        self.root.geometry(self.get_start_window_size())  # sets window size based on monitor resolution
        self.root.title('League Doc')
        self.root.configure(bg=color_scheme['root'])

        # packed frame
        self.centered_frame = Frame(self.root, width=self.width, height=self.height, bg=color_scheme['dark'])
        self.centered_frame.place(in_=self.root, anchor="c", relx=.5, rely=.5)

        # running app frame is the frame where the currently selected application displays.
        self.running_app_frame = self.create_running_app_frame()
        self.raf_width = int(self.width - (self.width / 5))
        self.raf_height = int(self.height)

        # app buttons
        self.apps_list_frame = Frame(self.centered_frame, bg=color_scheme['light'])
        self.app_label_frame = Frame(self.apps_list_frame, width=(int(self.width / 5)), height=int(self.height / 12),
                                     bg=color_scheme['dark'])
        self.app_label = Label(self.app_label_frame, text="Apps", bg=color_scheme['light'])
        self.app_label_frame.propagate(False)
        self.app_label_frame.grid(row=0, column=0)
        self.app_label.pack(expand=True, fill=BOTH)

    def config_raf_height(self, height):
        self.running_app_frame.configure(height=height)
        self.raf_height = height
        self.set_scroll_region_size(self.width, self.height)

    # creates the running app frame allowing for scrollbar implementation.
    def create_running_app_frame(self):
        canvas_frame = Frame(self.centered_frame, width=int(self.width - (self.width / 5)), height=int(self.height),
                             bg=color_scheme['dark'])
        canvas = Canvas(canvas_frame, bg=color_scheme['dark'])
        running_app_frame = Frame(canvas, bg=color_scheme['dark'])
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview, bg=color_scheme['dark'])
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill='y')
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=running_app_frame, anchor='nw')
        running_app_frame.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox('all'),
                                                               width=int(self.width - (self.width / 5) - 20),
                                                               height=int(self.height) - 20))
        canvas.configure(scrollregion=(0, 0, int(self.width - (self.width / 5) - 20), int(self.height) - 20),
                         bg=color_scheme['dark'])

        canvas_frame.grid_propagate(0)
        canvas_frame.grid(row=0, column=1)
        return running_app_frame

    # empties the running app frame. Generally used when switching applications.
    def clear_running_app_frame(self):
        for widgets in self.running_app_frame.winfo_children():
            widgets.destroy()
        self.height = self.default_height

    # updates the favorite app buttons on the left side of the root window
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
                bg=color_scheme['dark_text'],
                fg=color_scheme['light_text'],
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
        self.clear_running_app_frame()
        if folder_name != "":
            my_module = importlib.import_module(folder_name)
            if folder_name =="Home":
                my_module.run(self)
            else:
                my_module.run(self)

    # retrieves the pixel resolution of the monitor and calculates the size of the root window.
    def get_start_window_size(self):
        w_res = GetSystemMetrics(0)
        h_res = GetSystemMetrics(1)

        self.height = int(h_res / 1.5)
        self.default_height = int(h_res / 1.5)
        self.width = int((w_res * self.height) / h_res)

        return f'{self.width}x{self.height}'

    # sets the total (vertical) scroll region for the running app frame
    def set_scroll_region_size(self, width, height):
        canvas = self.get_parent_widget(self.running_app_frame)
        canvas.configure(scrollregion=(0, 0, width, height))

    # returns the widget(s) underneath the passed widget
    @staticmethod
    def get_child_widget(widget):
        widget_name = widget.winfo_child()
        child = Widget._nametowidget(widget, name=widget_name)
        return child

    # returns the widget the passed widgets is directly inside of
    # ie: frame = new Frame(parent) and frame is passed through, the widget stored in parent would be returned.
    @staticmethod
    def get_parent_widget(widget):
        widget_name = widget.winfo_parent()
        parent = Widget._nametowidget(widget, name=widget_name)
        return parent
