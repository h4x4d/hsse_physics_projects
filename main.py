from vpython import rate

from objects.canvas import Canvas
from objects.coordinates import Coordinates
from objects.earth import Earth
from objects.ISS import ISSOrbit
from objects.rocket import Rocket

canvas = Canvas()
coordinates_system = Coordinates(10 ** len(str(Earth.RADIUS)))
iss_orbit = ISSOrbit()
earth = Earth()

rocket = Rocket(canvas.canvas)
canvas.canvas.range = 1000

input("START:")

while True:
    rate(10**5)
    rocket.update(1)

