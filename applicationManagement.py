import importlib
import os
import sys
import tkinter as tk


# imports the applications code from its file and executes it
def run_applications(folder_name):
    my_module = importlib.import_module(folder_name)
    my_module.run(tk)


# creates an array for all the applications, specified with folders not including '.'
def get_apps():
    apps = []
    files = os.listdir()
    for file in files:
        if "___" not in file:
            pass
        else:
            apps.append(file)
            path = os.getcwd()+"\\"+file
            sys.path.append(path)
    return apps
