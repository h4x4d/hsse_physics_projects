from vpython import sphere, vector, textures


class Earth:
    RADIUS = 6378 * 1000
    MASS = 5.9722 * 10 ** 24
    CENTER_COORDS = vector(0, 0, 0)
    FREE_FALL_ACCELERATION = 9.81
    GRAVITATIONAL_CONSTANT = 6.6743 * (10 ** (-11))

    def __init__(self):
        self.object = sphere(pos=self.CENTER_COORDS,
                             radius=self.RADIUS,
                             texture=textures.earth)

    def update(self):
        # earth is not rotating now
        ...
