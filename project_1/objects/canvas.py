from vpython import canvas


class Canvas:
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self, attach_range):
        self.canvas = canvas(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.select()

        if attach_range:
            self.canvas.range = attach_range

    def load_info(self, title, info):
        self.canvas.title = title
        self.canvas.caption = info
