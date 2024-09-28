import csv

from objects.earth import Earth


class Logger:
    def __init__(self, log_file_name):
        self.log_file = csv.writer(open(log_file_name, 'w', encoding='utf-8'))
        self.log_file.writerow(["status", "mass", "fuel_mass", "pos", "height",
                                "speed", "speed_mag", "acceleration", "time"])

    def log_info(self, rocket, ticks):
        self.log_file.writerow([rocket.status.name, rocket.mass,
                                rocket.fuel_mass, rocket.pos,
                                rocket.height,
                                rocket.speed, rocket.speed.mag,
                                rocket.acceleration, ticks])
