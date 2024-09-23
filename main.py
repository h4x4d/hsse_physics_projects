from objects.canvas import Canvas
from objects.coordinates import Coordinates
from objects.earth import Earth
from objects.ISS import ISSOrbit

canvas = Canvas()
coordinates_system = Coordinates(10 ** len(str(Earth.RADIUS)))
iss_orbit = ISSOrbit()
earth = Earth()


