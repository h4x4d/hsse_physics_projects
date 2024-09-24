import argparse

from logs.log_info import log_info

parser = argparse.ArgumentParser(
    prog="Rocket starter",
    description="Send rocket to space using simple python app!",
)
parser.add_argument("-a", "--attach",
                    help="Attach camera to rocket",
                    action="store_true")

parser.add_argument("-s", "--step",
                    help="How many seconds in one step (default: 1)",
                    default=1, )

parser.add_argument("-r", "--rate",
                    help="How many steps in one second (default: 30)",
                    default=30, )

parser.add_argument("-t", "--trail",
                    help="Size of trail (0-100000) (default: 1000)",
                    default=1000, )

parser.add_argument("-m", "--max",
                    help="Max amount of ticks (default: 1000)",
                    default=1000, )

parser.add_argument("-l", "--logging",
                    help="Log rocket status",
                    action="store_true")


def run(attach, dt, framerate, trail, maximum, logging):
    from vpython import rate

    from objects.canvas import Canvas
    from objects.coordinates import Coordinates
    from objects.earth import Earth
    from objects.ISS import ISSOrbit
    from objects.rocket import Rocket
    from logs.render_logs import render_logs

    canvas = Canvas((trail * 100 if trail else 1000) if attach else 0)

    Coordinates(10 ** len(str(Earth.RADIUS)))
    ISSOrbit()
    earth = Earth()

    rocket = Rocket(canvas.canvas if attach else None, trail)

    ticks = 0

    while ticks < maximum:
        rate(framerate)
        ticks += dt
        earth.update(dt)
        rocket.update(dt)
        canvas.load_info(*render_logs(rocket, ticks))
        if logging:
            log_info(rocket, ticks)


if __name__ == '__main__':
    args = parser.parse_args()

    run(args.attach, int(args.step), int(args.rate),
        int(args.trail), int(args.max), args.logging)
