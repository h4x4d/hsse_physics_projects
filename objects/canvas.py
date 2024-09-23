from vpython import canvas, vector


class Canvas:
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self):
        self.canvas = canvas(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.select()
