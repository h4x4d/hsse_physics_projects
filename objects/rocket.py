from operator import length_hint

from mistune.plugins.ruby import parse_ruby
from vpython import vector, arrow, color, cone
from math import sin, cos, radians

from objects.earth import Earth


class Rocket:
    MASS = 6650

    def __init__(self, camera):
        self.axis = vector(cos(radians(51)) * 10, sin(radians(51)) * 10, 0)
        self.pos = vector(cos(radians(51)) * Earth.RADIUS, sin(radians(51)) * Earth.RADIUS, 0)  - vector(16060, 16060, 0)

        self.object = cone(
            pos=self.pos,
            axis=self.axis,
            color=color.white,
            radius=25,
            length=50,
            make_trail=True,
            trail_radius=10
        )

        camera.follow(self.object)


    def update(self):
        self.object.pos += vector(cos(radians(51)), sin(radians(51)), 0)