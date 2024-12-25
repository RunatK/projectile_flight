class ThetaInterval:
    __slots__ = (
        'theta',
        't',
        'x1',
        'x2'
    )

    def __init__(self, theta: float, t: float, x1: float, x2: float):
        self.theta = theta
        self.t = t
        self.x1 = x1
        self.x2 = x2