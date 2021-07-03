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
    scroll_region_height = 0

    # creates sorting frames
    options_frame = Frame(app_frame)
    options_frame.grid(row=0, column=0)
    app_boxes_frame = Frame(app_frame)
    app_boxes_frame.grid(row=1, column=0)

    # app favoriting section
    app_fav_section = Label(app_frame, text="Fav Apps")
    app_fav_section_advice = Label(app_frame, text="Choose up to five")
    app_fav_section.grid(row=0, column=2)
    app_fav_section_advice.grid(row=1, column=2)

    # puts checkboxes on app boxes
    checkbox_variables = []
    apps = Am.get_apps()
    fav_apps = Am.get_favorite_apps()
    counter = 0
    row_counter = 1
    col_counter = 0
    fav_app_counter = 1
    for app in apps:
        if not app == "___Home":
            if app != fav_apps[fav_app_counter]:
                checkbox_variables.append(IntVar())
            else:
                if fav_app_counter < len(fav_apps) - 1:
                    fav_app_counter += 1
                checkbox_variables.append(IntVar(value=1))
            app_boxes.append(create_app_box(gui, app[3:], 10 + col_counter, row_counter))
            Checkbutton(app_boxes[counter], variable=checkbox_variables[counter],
                        fg='DarkGray', bg='DarkGray').pack(side=BOTTOM)
            counter += 1
            if row_counter == 3:
                row_counter = 1
                col_counter += 1
            else:
                row_counter += 1
    favoriting_button = Button(app_frame, text="Set Favorites", command=lambda: favoring_apps(checkbox_variables,
                                                                                              app_fav_section_advice,
                                                                                              gui))
    favoriting_button.grid(row=2, column=2)

    # app adding section
    app_adder_text = Label(app_frame, text="Add new apps here")
    app_adder_button = Button(app_frame,
                              text="Add App",
                              command=lambda text=app_adder_text: browse_files(text))
    app_adder_text.grid(row=0, column=1)
    app_adder_button.grid(row=2, column=1)

    # increases scroll region size to fit # of app boxes
    if len(app_boxes) / 3 > 4:
        gui.set_scroll_region_size(int(gui.width - (gui.width / 5) - 20), int(gui.height) - 20 +
                                   (((int(int(gui.width - (gui.width / 5)) / 3) - 100) / 2.41) * (len(app_boxes) / 3 - 3)))


def create_app_box(gui, name, row, col):
    # get the main app frame
    app_frame = gui.running_app_frame
    app_frame_width = int(gui.width - (gui.width / 5))

    # create the app box
    frame = Frame(app_frame, bg='DarkGray', width=int(app_frame_width / 3) - 100, height=(int(app_frame_width / 3) - 100) / 2.41)
    frame.pack_propagate(0)

    # create name_label
    name_label = Label(frame, text=name, fg='Black', bg='DarkGray')
    name_label.pack(pady=5, side=TOP)

    # inserts the app box
    frame.grid(row=row, column=col, padx=50, pady=15)

    return frame


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
        advice.configure(text="You can not favorite more than 5 apps.")
    else:
        while len(favs) < 6:
            favs.append("___")
        with open("favoriteApps.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(favs)
        advice.configure(text="Favorites Added")
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
