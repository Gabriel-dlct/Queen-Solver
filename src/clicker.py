from Xlib import display, X
from Xlib.ext.xtest import fake_input
import time
import random

dpy = display.Display()

def send_click(x, y):
    fake_input(dpy, X.MotionNotify, x=x, y=y)
    for _ in range(2):
        fake_input(dpy, X.ButtonPress, 1)
        time.sleep(random.uniform(0.1, 0.15))
        fake_input(dpy, X.ButtonRelease, 1)
    dpy.sync()


def clicker(screen_dim, game_dim, queen_pos):
    x, y, w, h = game_dim

    width = w // len(queen_pos)

    x_pos = x + width//2
    y_pos = y + width //2

    for i in range(len(queen_pos)):
        send_click(x=x_pos, y=(y_pos + width * queen_pos[i]))  
        time.sleep(random.uniform(0.1, 0.15))
        x_pos += width 

    dpy.sync()



    