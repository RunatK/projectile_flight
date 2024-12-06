import numpy as np

from src.projectile_flight import ProjectileFlight
from matplotlib import pyplot as plt


g = 9.8


def function(t: list[float], y: list[float]):
    x1, x2, x3, x4 = y
    dydt = np.array([x3, x4 , 0.0, -g])
    return dydt


def surface(x: float):
    return np.cos(x)


if __name__ == "__main__":
    K = 10
    m = 1
    theta = np.pi/4
    v_0 = np.sqrt(2*K/m)
    y0 = [0.0, surface(0.0), v_0*np.cos(theta), v_0*np.sin(theta)]
    t = np.linspace(0, 10, 1001)
    h = t[1] - t[0]
    project_flight = ProjectileFlight(surface, h)
    result = project_flight.run(
        f = function,
        y_start = y0,
        t = t
    )
    x_1_result = project_flight.get_polynomial_value_x1(result)
    x_2_result = project_flight.get_polynomial_value_x2(result)
    print(f"t result: {result}. x1 result: {x_1_result}. x2 result {x_2_result}")