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

    root.mainloop()

t2 = threading.Thread(target=data_collection, args=())
t1 = threading.Thread(target=gui, args=())
t1.start()
t2.start()
t1.join()
t2.join()
