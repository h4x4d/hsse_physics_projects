from vpython import sphere, vector, color, rotate, rate, attach_trail, textures, canvas, arrow


class Earth:
    RADIUS = 6378 * 1000
    MASS = 5.9722 * 10 ** 24
    CENTER_COORDS = vector(0, 0, 0)

    def __init__(self):
        self.object = sphere(pos=self.CENTER_COORDS,
                             radius=self.RADIUS,
                             texture=textures.earth)


    def update(self):
        ...