from vpython import sphere, vector, textures
from math import radians


class Earth:
    RADIUS = 6378 * 1000
    MASS = 5.9722 * 10 ** 24
    CENTER_COORDS = vector(0, 0, 0)
    FREE_FALL_ACCELERATION = 9.81
    GRAVITATIONAL_CONSTANT = 6.6743 * (10 ** (-11))
    ANGULAR_SPEED = 7.2921158553 * (10 ** (-5))

    def __init__(self):
        self.object = sphere(pos=self.CENTER_COORDS,
                             radius=self.RADIUS,
                             texture=textures.earth)

    def update(self, dt):
        self.object.rotate(radians(1 / 240 * dt), axis=vector(0, 1, 0))
