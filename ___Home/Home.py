from tkinter import filedialog
from tkinter import *
import shutil
import os
import applicationManagement
lastUpdateAppList = []
def run(tk, app_frame):
    global lastUpdateAppList
    #print(f'{app_frame.winfo_width()}, {app_frame.winfo_height()}')
    #for i in range(100):
    #    tk.Label(app_frame, text="app ran").grid(row=i, column=0)
    lastUpdateAppList = applicationManagement.get_apps()

    #app adding section
    appAdderText = Label(app_frame, text="Add new apps here")
    appAddeButton = Button(app_frame,
                            text="Add App",
                            command=lambda text=appAdderText: browseFiles(appAdderText))
    appAdderText.grid(row=1, column=1)
    appAddeButton.grid(row=2, column=1)

def browseFiles(appAdderText):
    #ask the user to find the folder
    dir_path = filedialog.askdirectory()
    #check if the folder has the signature ___ and if so copy it to current directory with its file name
    if "___" in dir_path:
        dir_name_location = dir_path.index("___")
        dir_name = dir_path[dir_name_location:len(dir_path)]
        appAdderText.configure(text="app added: " + dir_name)
        try:
            shutil.copytree(dir_path, os.getcwd()+"\\"+dir_name)
        except:
            appAdderText.configure(text="Error file already exists " + dir_name)
    else:
        appAdderText.configure(text="unrecgonized file, be sure to add the file with ___ at the start")


