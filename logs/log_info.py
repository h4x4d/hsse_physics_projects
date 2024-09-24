import csv

from objects.earth import Earth

log_file = csv.writer(open('logs.csv', 'w', encoding='utf-8'))
log_file.writerow(["status", "mass", "fuel_mass", "pos", "height", "speed", "speed_mag", "acceleration", "time"])


def log_info(rocket, ticks):
    log_file.writerow([rocket.status.name, rocket.mass,
                       rocket.fuel_mass, rocket.pos,
                       ((rocket.pos).mag - Earth.RADIUS),
                       rocket.speed, rocket.speed.mag,
                       rocket.acceleration, ticks])
