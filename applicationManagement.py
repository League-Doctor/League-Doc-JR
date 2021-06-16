import os
import sys
import csv

# creates an array for all the applications, specified with folders not including '.'
def get_favorited_apps():
    fav_apps = []
    #if it dosnt exist build a file with only home as its fav
    if not os.path.isfile("favoriteApps.csv"):
        fav_apps.append("___Home")
        fav_apps.append("___")
        fav_apps.append("___")
        fav_apps.append("___")
        fav_apps.append("___")
        fav_apps.append("___")
        with open("favoriteApps.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(fav_apps)

    else:
        with open("favoriteApps.csv", "r") as file:
            line_reader = csv.reader(file)
            for line in line_reader:
                for app in line:
                    fav_apps.append(app)
    return fav_apps
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
    apps.remove('___Home')
    apps.append('___Home')
    apps.reverse()
    return apps
