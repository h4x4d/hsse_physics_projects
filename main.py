from vpython import rate

from objects.canvas import Canvas
from objects.coordinates import Coordinates
from objects.earth import Earth
from objects.ISS import ISSOrbit
from objects.rocket import Rocket
from render_logs import render_logs

canvas = Canvas()
coordinates_system = Coordinates(10 ** len(str(Earth.RADIUS)))
iss_orbit = ISSOrbit()
earth = Earth()

rocket = Rocket(canvas.canvas)
canvas.canvas.range = 1000

# input("START:")
ticks = 0
dt = 1

while True:
    rate(20)
    ticks += dt
    values = rocket.update(dt)
    canvas.load_info(*render_logs(rocket, ticks))

