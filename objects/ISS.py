from math import cos, sin, radians, sqrt

from vpython import vector, ring, color, sphere, textures

from objects.earth import Earth

"""
class ISSOrbit:
    CENTER = vector(0, 0, 0)
    AXIS = vector(-sin(radians(51)) * 10 ** 5, cos(radians(51)) * 10 ** 5, 0)
    RADIUS = Earth.RADIUS + 400 * 1000

    def __init__(self):
        self.object = ring(pos=self.CENTER, axis=self.AXIS, radius=self.RADIUS,
                           tickness=10, color=color.yellow,
                           size=vector(10 ** 8, 10 ** 8, 10 ** 8))
"""


class ISS:
    ORBIT = Earth.RADIUS + 400 * 1000
    START_POS = vector(cos(radians(51)) * ORBIT,
                       sin(radians(51)) * ORBIT, 0)
    ORBIT_AXIS = vector(-sin(radians(51)), cos(radians(51)), 0)
    CENTER = vector(0, 0, 0)
    RADIUS = 100000

    SPEED_MAG = ((sqrt(Earth.GRAVITATIONAL_CONSTANT
                       * Earth.MASS / ORBIT)))

    # Создаем статический объект сферы
    object = sphere(pos=START_POS, radius=RADIUS, texture=textures.rough)

    # Статическая скорость объекта
    speed = object.pos.cross(ORBIT_AXIS).hat * SPEED_MAG

    @staticmethod
    def update(dt):
        # Обновляем скорость
        ISS.speed -= (ISS.object.pos.hat *
                      ((Earth.GRAVITATIONAL_CONSTANT *
                        Earth.MASS / ISS.object.pos.mag2) * dt))
        # Обновляем позицию объекта
        ISS.object.pos += ISS.speed * dt
