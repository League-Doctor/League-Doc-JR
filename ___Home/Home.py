from tkinter import filedialog
from tkinter import *
import shutil
import os
import applicationManagement
import csv
lastUpdateAppList = []
def run(app_frame):
    global lastUpdateAppList
    #print(f'{app_frame.winfo_width()}, {app_frame.winfo_height()}')
    #for i in range(100):
    #    Label(app_frame, text="app ran").grid(row=i, column=0)

    #app favoriting section
    app_fav_section = Label(app_frame, text="Fav Apps")
    app_fav_section_advice = Label(app_frame, text="Choose up to five")
    app_fav_section.grid(row=0, column =2)
    app_fav_section_advice.grid(row=1, column=2)
    counter = 0
    checkboxVariables = []
    for app in applicationManagement.get_apps():
        if not app == "___Home":
            checkboxVariables.append(IntVar())
            Checkbutton(app_frame, text=app[3:], variable=checkboxVariables[counter]).grid(row=counter+2, column=2)
            counter += 1
    favoring_button = Button(app_frame,
                              text="set Favs",
                              command=lambda text=checkboxVariables: favoring_apps(text,app_fav_section_advice))
    favoring_button.grid(row=counter+2, column=2)


    #app adding section
    app_adder_text = Label(app_frame, text="Add new apps here")
    app_adder_Button = Button(app_frame,
                            text="Add App",
                            command=lambda text=app_adder_text: browse_files(text))
    app_adder_text.grid(row=1, column=1)
    app_adder_Button.grid(row=2, column=1)



def favoring_apps(checkboxes,advice):
    count = 0
    counter = 0
    currentApps = applicationManagement.get_apps()
    favs = ["___Home"]
    for checkbox in checkboxes:
        if checkbox.get() == 1:
            count +=1
            favs.append(currentApps[counter+1])
        counter += 1
    if count > 6:
        advice.configure(text="You have Entered more than 5")
    else:
        while len(favs) <6:
            favs.append("___")
        with open("favoriteApps.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(favs)
        advice.configure(text="favs added")


def browse_files(app_adder_text):
    #ask the user to find the folder
    dir_path = filedialog.askdirectory()
    #check if the folder has the signature ___ and if so copy it to current directory with its file name
    if "___" in dir_path:
        dir_name_location = dir_path.index("___")
        dir_name = dir_path[dir_name_location:len(dir_path)]
        app_adder_text.configure(text="app added: " + dir_name)
        try:
            shutil.copytree(dir_path, os.getcwd()+"\\"+dir_name)
        except:
            app_adder_text.configure(text="Error file already exists " + dir_name)
    else:
        app_adder_text.configure(text="unrecgonized file, be sure to add the file with ___ at the start")


