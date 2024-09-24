import enum
from vpython import vector, color, cone
from math import sin, cos, radians, pi, sqrt, exp

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
    START_POS = (vector(cos(radians(51)) * Earth.RADIUS,
                        sin(radians(51)) * Earth.RADIUS, 0)
                 - vector(16060, 16060, 0))

    def __init__(self, camera, trail_radius):
        axis = vector(cos(radians(51)) * 10, sin(radians(51)) * 10, 0)
        self.acceleration_hat = axis.hat

        self.pos = self.START_POS

        self.speed = (self.pos.cross(vector(0, 1, 0)).hat * Earth.ANGULAR_SPEED * Earth.RADIUS)

        self.object = cone(
            pos=self.pos,
            axis=axis,
            color=color.white,
            radius=25,
            length=50,
            make_trail=True,
            trail_radius=trail_radius
        )

        self.acceleration = 0
        self.fuel_mass = 6000

        self.status = Status.TAKEOFF

        if camera:
            camera.follow(self.object)

    @property
    def mass(self):
        return self.MASS + self.fuel_mass

    def gravity_force(self):
        return (Earth.GRAVITATIONAL_CONSTANT *
                Earth.MASS * self.mass / self.pos.mag2)

    def update_takeoff(self, dt):
        acceleration = Earth.FREE_FALL_ACCELERATION * 4
        free_fall_acceleration = (self.gravity_force() / self.mass)
        need_acceleration = acceleration + free_fall_acceleration

        spent_fuel = need_acceleration * self.mass / self.GAS_SPEED
        self.fuel_mass -= spent_fuel * dt

        if self.fuel_mass <= 0:
            self.status = Status.NO_FUEL

        self.acceleration = acceleration
        self.speed += self.acceleration_hat * (self.acceleration * dt)
        self.pos += self.speed * dt

        inertia_distance = self.speed.mag2 / (2 * free_fall_acceleration)

        if self.pos.mag + inertia_distance >= Earth.RADIUS + 200 * 1000:
            self.status = Status.INERTIA

        self.object.pos = self.pos

    def update_inertia(self, dt):
        need_vec = self.pos.cross(vector(0, 1, 0))
        diff_angle = need_vec.diff_angle(self.object.axis)
        self.object.rotate(max(0.0, min(pi / 12, diff_angle)),
                           vector(sin(radians(51)), -cos(radians(51)), 0))

        free_fall_acceleration = (self.gravity_force() / self.mass)
        self.speed += self.acceleration_hat * (-free_fall_acceleration * dt)
        if self.speed.x <= 0 and self.speed.y <= 0:
            self.status = Status.ORBIT
            self.speed = vector(0, 0, 0)
            self.raise_speed()
            return

        self.pos += self.speed * dt
        self.object.pos = self.pos

    def raise_speed(self):
        self.speed = self.pos.cross(vector(0, 1, 0)).hat
        self.speed *= sqrt(Earth.GRAVITATIONAL_CONSTANT
                           * Earth.MASS / self.pos.mag)
        self.fuel_mass -= (self.mass *
                           (1 - exp(-(self.speed.mag / self.GAS_SPEED))))
        print(self.speed.mag, self.fuel_mass)

    def update_orbit(self, dt):
        need_vec = self.pos.cross(vector(0, 1, 0))

        self.pos += self.speed * dt
        self.object.pos = self.pos

        free_fall_acceleration = (self.gravity_force() / self.mass)
        self.speed -= (self.pos.hat *
                       (free_fall_acceleration * dt))
        self.object.rotate(self.object.axis.diff_angle(need_vec),
                           vector(sin(radians(51)), -cos(radians(51)), 0))

    def update(self, dt):
        if self.status == Status.TAKEOFF:
            self.update_takeoff(dt)
        elif self.status == Status.INERTIA:
            self.update_inertia(dt)
        elif self.status == Status.ORBIT:
            self.update_orbit(dt)
        elif self.status == Status.NO_FUEL:
            print("NO FUEL")
            raise ValueError("NO FUEL")
