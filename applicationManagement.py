import os
import sys

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
    apps.remove('___Home')
    apps.append('___Home')
    apps.reverse()
    return apps
