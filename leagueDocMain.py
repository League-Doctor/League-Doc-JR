from tkinter import *
from frameworkGUI import GUI
import subprocess
import threading


def data_collection():
    subprocess.call("pythonw.exe dataCollector.py", shell=False)


def gui():
    root = Tk()

    gui = GUI(root)
    gui.show_app_buttons()
    gui.run_applications('Home')

    root.mainloop()


# this threading code was originally intended to allow for passive data collection (auto detection of entering champion
# selection while the app is running. This will most likely be changed in the future due to not having used the feature.
t2 = threading.Thread(target=data_collection, args=())
t1 = threading.Thread(target=gui, args=())
t1.start()
t2.start()
t1.join()
t2.join()
