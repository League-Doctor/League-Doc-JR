from tkinter import filedialog
from tkinter import *
import shutil
import os
import applicationManagement as Am
import csv

lastUpdateAppList = []


def run(gui):

    global lastUpdateAppList
    app_frame = gui.running_app_frame
    app_boxes = []
    app_frame_width = int(gui.width - (gui.width / 5))
    app_frame_height = int(gui.height)
    # print(f'{app_frame_width}, {app_frame_height}')
    scroll_region_height = 0
    """
    
    Test for scroll region sizing
    
    for i in range(50):
        label_frame = Frame(app_frame, width=60, height=50, bg='white', pady=10, padx=2)
        scroll_region_height += 50
        label_frame.pack_propagate(0)
        label = Label(label_frame, fg='black', text="app ran")
        label.pack()
        label_frame.grid(row=i, column=0)
    gui.set_scroll_region_size(gui.width, scroll_region_height)
    
    """

    # app favoriting section
    app_fav_section = Label(app_frame, text="Fav Apps")
    app_fav_section_advice = Label(app_frame, text="Choose up to five")
    app_fav_section.grid(row=0, column=2)
    app_fav_section_advice.grid(row=1, column=2)
    counter = 0
    checkbox_variables = []
    for app in Am.get_apps():
        if not app == "___Home":
            checkbox_variables.append(IntVar())
            Checkbutton(app_frame, text=app[3:], variable=checkbox_variables[counter]).grid(row=counter + 2, column=2)
            counter += 1
    favoring_button = Button(app_frame,
                             text="Set Favorites",
                             command=lambda text=checkbox_variables: favoring_apps(text, app_fav_section_advice, gui))
    favoring_button.grid(row=counter + 2, column=2)

    # app adding section
    app_adder_text = Label(app_frame, text="Add new apps here")
    app_adder_button = Button(app_frame,
                              text="Add App",
                              command=lambda text=app_adder_text: browse_files(text))
    app_adder_text.grid(row=1, column=1)
    app_adder_button.grid(row=2, column=1)
    create_app_box(gui, 'TEST', 10, 1)
    create_app_box(gui, 'TEST', 10, 2)
    create_app_box(gui, 'TEST', 10, 3)


def create_app_box(gui, name, row, col):
    # get the main app frame
    app_frame = gui.running_app_frame
    app_frame_width = int(gui.width - (gui.width / 5))

    # create the app box
    frame = Frame(app_frame, bg='DarkGray', width=int(app_frame_width / 3) - 100, height=100)
    frame.pack_propagate(0)

    # create name_label
    name_label = Label(frame, text=name, fg='LightGray', bg='DarkGray')
    name_label.pack(pady=5, side=TOP)

    # inserts the app box
    frame.grid(row=row, column=col, padx=50, pady=15)


def favoring_apps(checkboxes, advice, gui):
    count = 0
    counter = 0
    current_apps = Am.get_apps()
    favs = ["___Home"]
    for checkbox in checkboxes:
        if checkbox.get() == 1:
            count += 1
            favs.append(current_apps[counter + 1])
        counter += 1
    if len(favs) > 6:
        advice.configure(text="You have Entered more than 5")
    else:
        while len(favs) < 6:
            favs.append("___")
        with open("favoriteApps.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(favs)
        advice.configure(text="favs added")
        gui.refresh_favorites(favs)


def browse_files(app_adder_text):
    # ask the user to find the folder
    dir_path = filedialog.askdirectory()
    # check if the folder has the signature ___ and if so copy it to current directory with its file name
    if "___" in dir_path:
        dir_name_location = dir_path.index("___")
        dir_name = dir_path[dir_name_location:len(dir_path)]
        app_adder_text.configure(text="app added: " + dir_name)
        try:
            shutil.copytree(dir_path, os.getcwd() + "\\" + dir_name)
        except:
            app_adder_text.configure(text="Error file already exists " + dir_name)
    elif '' == dir_path:
        app_adder_text.configure(text="Add new apps here")
    else:
        app_adder_text.configure(text="unrecognized file, be sure to add the file with ___ at the start")
