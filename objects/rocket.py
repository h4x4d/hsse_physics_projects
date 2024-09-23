import enum
from operator import length_hint

from jedi.debug import speed
from mistune.plugins.ruby import parse_ruby
from vpython import vector, arrow, color, cone
from math import sin, cos, radians

from objects.earth import Earth


class Status(enum.Enum):
    TAKEOFF = 1
    INERTIA = 2
    SPINNING = 3
    ORBIT = 4
    NO_FUEL = 100


class Rocket:
    MASS = 1000
    GAS_SPEED = 8000
    START_POS = vector(cos(radians(51)) * Earth.RADIUS, sin(radians(51)) * Earth.RADIUS, 0) - vector(16060, 16060, 0)

    def __init__(self, camera):
        self.axis = vector(cos(radians(51)) * 10, sin(radians(51)) * 10, 0)
        self.pos = self.START_POS

        self.speed = vector(0, 0, 0)

        self.object = cone(
            pos=self.pos,
            axis=self.axis,
            color=color.white,
            radius=25,
            length=50,
            make_trail=True,
            trail_radius=10 # 000
        )

        self.acceleration = 0
        self.fuel_mass = 6000

        self.status = Status.TAKEOFF

        camera.follow(self.object)

    @property
    def mass(self):
        return self.MASS + self.fuel_mass

    def gravity_force(self):
        return Earth.GRAVITATIONAL_CONSTANT * Earth.MASS * self.mass / self.pos.mag2

    def update_takeoff(self, dt):
        acceleration = Earth.FREE_FALL_ACCELERATION * 4
        free_fall_acceleration = (self.gravity_force() / self.mass)
        need_acceleration = acceleration + free_fall_acceleration
        print(need_acceleration)

        spent_fuel = need_acceleration * self.mass / self.GAS_SPEED
        self.fuel_mass -= spent_fuel * dt

        if self.fuel_mass <= 0:
            self.status = Status.NO_FUEL

        self.acceleration = acceleration
        self.speed += self.axis / self.axis.mag * (self.acceleration * dt)
        self.pos += self.speed * dt

        inertia_distance = (self.speed.mag2) / (2 * free_fall_acceleration)

        if self.pos.mag + inertia_distance >= Earth.RADIUS + 200 * 1000:
            self.status = Status.INERTIA
            print(f"INERTIA: {self.pos.mag - (vector(cos(radians(51)) * Earth.RADIUS, sin(radians(51)) * Earth.RADIUS, 0) - vector(16060, 16060, 0)).mag}, {self.speed.mag}, {inertia_distance}")

        self.object.pos = self.pos

    def update_inertia(self, dt):
        # need_vec = self.pos.cross(vector(0, 1, 0)) / self.pos.cross(vector(0, 1, 0)).mag
        free_fall_acceleration = (self.gravity_force() / self.mass)
        print(self.speed.mag, free_fall_acceleration)
        self.speed += self.axis / self.axis.mag * (-free_fall_acceleration * dt)
        if all(i <= 0 for i in self.speed.value):
            self.status = Status.ORBIT
            self.speed = vector(0, 0, 0)
            return

        self.pos += self.speed * dt
        self.object.pos = self.pos


    def update(self, dt):
        if self.status == Status.TAKEOFF:
            self.update_takeoff(dt)
        elif self.status == Status.INERTIA:
            self.update_inertia(dt)
        elif self.status == Status.NO_FUEL:
            print("NO FUEL")
            raise 1