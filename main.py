import argparse

from logs.logger import Logger

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
                    default="")

parser.add_argument("--stop",
                    help="Stop on reached maximum",
                    action="store_true")


def run(attach, dt, framerate, trail, maximum, log_file, stop):
    from objects.canvas import Canvas
    canvas = Canvas((trail * 100 if trail else 1000) if attach else 0)

    from vpython import rate
    from vpython.no_notebook import stop_server

    from objects.coordinates import Coordinates
    from objects.earth import Earth
    from objects.ISS import ISS
    from objects.rocket import Rocket
    from logs.render_logs import render_logs


    Coordinates(10 ** len(str(Earth.RADIUS)))
    earth = Earth()

    rocket = Rocket(canvas.canvas if attach else None, trail)

    ticks = 0

    logger = None
    if log_file:
        logger = Logger(log_file)

    while ticks < maximum:
        rate(framerate)
        ticks += dt
        earth.update(dt)
        rocket.update(dt)
        ISS.update(dt)
        canvas.load_info(*render_logs(rocket, ticks))

        if logger:
            logger.log_info(rocket, ticks)

    if stop:
        stop_server()


if __name__ == '__main__':
    args = parser.parse_args()

    run(args.attach, float(args.step), int(args.rate),
        int(args.trail), int(args.max), args.logging, int(args.stop))
