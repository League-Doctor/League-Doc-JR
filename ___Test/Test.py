from tkinter import *


def run(gui):
    app_frame = gui.running_app_frame
    app_frame_width = int(gui.width - (gui.width / 5))
    app_frame_height = int(gui.height)

    test_button = Button(app_frame, text='test')
    test_button.pack()