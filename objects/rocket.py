import enum
from vpython import vector, color, cone
from math import sin, cos, radians, pi, sqrt, exp

from objects.earth import Earth


class Status(enum.Enum):
    TAKEOFF = 1
    INERTIA = 2
    RAISING_SPEED = 3
    ORBIT = 4
    HOHMANN = 5
    NO_FUEL = 100


class Rocket:
    MASS = 1000
    GAS_SPEED = 8000
    START_POS = (vector(cos(radians(51)) * Earth.RADIUS,
                        sin(radians(51)) * Earth.RADIUS, 0)
                 - vector(16060, 16060, 0))
    ORBIT_AXIS = vector(-sin(radians(51)) * 1, cos(radians(51)) * 1, 0)

    def __init__(self, camera, trail_radius):
        axis = vector(cos(radians(51)) * 10, sin(radians(51)) * 10, 0)
        self.acceleration_hat = axis.hat

        self.pos = self.START_POS

        self.speed = (self.pos.cross(vector(0, 1, 0)).hat *
                      Earth.ANGULAR_SPEED * Earth.RADIUS)

        self.object = cone(
            pos=self.pos,
            axis=axis,
            color=color.white,
            radius=25,
            length=50,
            make_trail=True if trail_radius > 0 else False,
            trail_radius=trail_radius
        )

        self.acceleration = 0
        self.fuel_mass = 6000

        self.status = Status.TAKEOFF

        self.timing = 0
        self.start_pos = vector(0, 0, 0)

        if camera:
            camera.follow(self.object)

    @property
    def mass(self):
        return self.MASS + self.fuel_mass

    @property
    def height(self):
        return self.pos.mag - Earth.RADIUS

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
        need_vec = self.pos.cross(self.ORBIT_AXIS)
        diff_angle = need_vec.diff_angle(self.object.axis)
        if diff_angle > 0.1:
            print("rotating rocket")
            self.object.rotate(max(0.0, min(dt * pi / 12, diff_angle)),
                               vector(sin(radians(51)), -cos(radians(51)), 0))
        else:
            self.status = Status.RAISING_SPEED

        free_fall_acceleration = (self.gravity_force() / self.mass)
        self.speed += self.acceleration_hat * (-free_fall_acceleration * dt)

        if self.speed.x <= 0 and self.speed.y <= 0:
            self.status = Status.ORBIT
            self.raise_speed()
            return

        self.pos += self.speed * dt
        self.object.pos = self.pos

    def update_raising_speed(self, dt):
        need_vec = self.pos.cross(self.ORBIT_AXIS).hat
        acc = 5 * Earth.FREE_FALL_ACCELERATION

        spent_fuel = acc * self.mass / self.GAS_SPEED

        self.fuel_mass -= spent_fuel * dt

        if self.fuel_mass <= 0:
            self.status = Status.NO_FUEL

        self.speed += need_vec * (acc * dt)

        free_fall_acceleration = (self.gravity_force() / self.mass)
        self.speed += self.acceleration_hat * (-free_fall_acceleration * dt)

        self.pos += self.speed * dt
        self.object.pos = self.pos

        self.last_angle = 0.0

        if self.height > 200 * 1000:
            self.raise_speed()
            self.status = Status.ORBIT
            return

    def orbital_speed(self, height):
        return ((sqrt(Earth.GRAVITATIONAL_CONSTANT
                      * Earth.MASS / height)))

    def raise_speed(self):
        new_speed = (self.pos.cross(self.ORBIT_AXIS).hat *
                     self.orbital_speed(self.pos.mag))
        self.fuel_mass -= (self.mass *
                           (1 - exp(-((new_speed.mag -
                                       self.speed.mag) / self.GAS_SPEED))))
        self.speed = new_speed

    def start_hohmann(self):
        second_speed = self.orbital_speed(Earth.RADIUS + 400 * 1000)
        first_speed = self.orbital_speed(Earth.RADIUS + 200 * 1000)
        speed_p = sqrt((first_speed ** 2 + second_speed ** 2) / 2)
        need_vec = self.pos.cross(self.ORBIT_AXIS).hat

        self.start_pos = self.pos

        self.speed += need_vec * (first_speed * (first_speed / speed_p - 1))

        self.fuel_mass = (self.mass /
                          (exp((first_speed * (first_speed / speed_p - 1))
                               / self.GAS_SPEED)) - self.MASS)

    def second_hohmann(self):
        second_speed = self.orbital_speed(Earth.RADIUS + 400 * 1000)
        first_speed = self.orbital_speed(Earth.RADIUS + 200 * 1000)
        speed_p = sqrt((first_speed ** 2 + second_speed ** 2) / 2)
        need_vec = self.pos.cross(self.ORBIT_AXIS).hat

        self.speed += need_vec * (second_speed * (1 - second_speed / speed_p))

        print(self.fuel_mass)
        self.fuel_mass = (self.mass /
                          (exp((second_speed * (1 - second_speed / speed_p))
                               / self.GAS_SPEED)) - self.MASS)
        print(self.fuel_mass)

    def update_on_orbit(self, dt):
        need_vec = self.pos.cross(self.ORBIT_AXIS)

        self.pos += self.speed * dt
        self.object.pos = self.pos

        free_fall_acceleration = (self.gravity_force() / self.mass)
        self.speed -= (self.pos.hat *
                       (free_fall_acceleration * dt))
        self.object.rotate(self.object.axis.diff_angle(need_vec),
                           vector(sin(radians(51)), -cos(radians(51)), 0))

    def update_orbit(self, dt):
        self.update_on_orbit(dt)

        self.timing += dt

        if self.timing >= 100:
            self.timing = -10 ** 9
            self.start_hohmann()
            self.status = Status.HOHMANN

    def update_hohmann(self, dt):
        self.update_on_orbit(dt)
        if self.pos.diff_angle(self.start_pos) < self.last_angle:
            self.second_hohmann()
            self.status = Status.ORBIT
        else:
            self.last_angle = self.pos.diff_angle(self.start_pos)

    def no_fuel(self, *_, **__):
        print("NO FUEL")
        raise ValueError("NO FUEL")

    def update(self, dt):
        statuses = {
            Status.TAKEOFF: self.update_takeoff,
            Status.INERTIA: self.update_inertia,
            Status.RAISING_SPEED: self.update_raising_speed,
            Status.ORBIT: self.update_orbit,
            Status.HOHMANN: self.update_hohmann,
            Status.NO_FUEL: self.no_fuel
        }
        statuses[self.status](dt)
