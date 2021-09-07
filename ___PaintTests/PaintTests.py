from datetime import time
from tkinter import *
import colorScheme as Cs

color_scheme = Cs.basic_color_scheme


def run(gui):

    raf = gui.running_app_frame
    gui.set_scroll_region_size(gui.raf_width, gui.raf_height + 300)
    # raf_height = 720:  (1920 X 1080 display)
    # raft_width = 1024: (1920 X 1080 display)

    drawing_canvas = Canvas(raf, width=gui.raf_width, height=gui.raf_height)
    drawing_canvas.pack()
    draw_button = Button(raf, text='draw', fg=color_scheme['light_text'], bg=color_scheme['dark_text'],
                         command=lambda: rectangle_fall(gui, drawing_canvas), font=90)
    draw_button.pack()


def rectangle_fall(gui, drawing_canvas):
    rect = drawing_canvas.create_rectangle(gui.raf_width / 2 + 100, gui.raf_height / 2 + 100,
                                           gui.raf_width / 2 - 100, gui.raf_height / 2 - 100,
                                           fill='black', width=3)
    print('drawn')
    movement(drawing_canvas, rect, 100)
    print('done')


def movement(drawing_canvas, rect, i):
    if i > 0:
        drawing_canvas.move(rect, 0, -10)
        drawing_canvas.after(100, movement(drawing_canvas, rect, i - 1))
