from vpython import vector, color, arrow


class Coordinates:
    X = vector(1, 0, 0)
    Y = vector(0, 1, 0)
    Z = vector(0, 0, 1)

    def __init__(self, scale):
        self.arrows = (
            arrow(axis=self.X * scale, shaftwidth=scale / 100, color=color.red),
            arrow(axis=self.Y * scale, shaftwidth=scale / 100, color=color.green),
            arrow(axis=self.Z * scale, shaftwidth=scale / 100, color=color.blue),
        )
