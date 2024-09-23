from math import cos, sin, radians

from vpython import vector, ring, color

from objects.earth import Earth


class ISSOrbit:
    CENTER = vector(0, 0, 0)
    AXIS = vector(-sin(radians(51)) * 10 ** 5, cos(radians(51)) * 10 ** 5, 0)
    RADIUS = Earth.RADIUS + 400 * 1000

    def __init__(self):
        self.object = ring(pos=self.CENTER, axis=self.AXIS, radius=self.RADIUS,
                           tickness=10, color=color.yellow,
                           size=vector(10 ** 8, 10 ** 8, 10 ** 8))
