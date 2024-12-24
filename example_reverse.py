import numpy as np

from src.reverse import ProjectileFlightReverse

g = 9.8

def ode(t: list[float], y: tuple[float, float, float, float]):
    x1, x2, x3, x4 = y
    dydt = np.array([x3, x4 , 0.0, -g])
    return dydt


def surface(x: float):
    return np.cos(x)


if __name__ == "__main__":
    t = 0
    projectile = ProjectileFlightReverse(surface)
    projectile.run(
        f = ode,
        t_start = t
    )
