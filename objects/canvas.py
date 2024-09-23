from vpython import canvas, vector
import random


class Canvas:
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self):
        self.canvas = canvas(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.select()


    def load_info(self, title, info):
        self.canvas.title = title
        self.canvas.caption = info