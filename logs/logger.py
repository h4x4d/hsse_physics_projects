import csv

from objects.earth import Earth


class Logger:
    def __init__(self):
        self.log_file = csv.writer(open('logs.csv', 'w', encoding='utf-8'))
        self.log_file.writerow(["status", "mass", "fuel_mass", "pos", "height",
                                "speed", "speed_mag", "acceleration", "time"])

    def log_info(self, rocket, ticks):
        self.log_file.writerow([rocket.status.name, rocket.mass,
                                rocket.fuel_mass, rocket.pos,
                                rocket.height,
                                rocket.speed, rocket.speed.mag,
                                rocket.acceleration, ticks])
