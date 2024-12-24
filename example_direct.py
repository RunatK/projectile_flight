import numpy as np

from src.direct import ProjectileFlightDirect


g = 9.8


def ode(t: list[float], y: tuple[float, float, float, float]):
    x1, x2, x3, x4 = y
    dydt = np.array([x3, x4 , 0.0, -g])
    return dydt


def surface(x: float):
    return x / 2


if __name__ == "__main__":
    K = 10
    m = 1
    theta = 0.75
    v_0 = np.sqrt(2*K/m)
    y0 = [0.0, surface(0.0), v_0*np.cos(theta), v_0*np.sin(theta)]
    t = 0
    h = 10**(-2)
    err = h**4
    project_flight = ProjectileFlightDirect(surface, err)
    result = project_flight.run(
        f = ode,
        y_start = y0,
        t_start = t,
        h = h
    )
    x_1_result = project_flight.get_polynomial_value_x1(result)
    x_2_result = project_flight.get_polynomial_value_x2(result)
    print(f"t result: {result}. x1 result: {x_1_result}. x2 result {x_2_result}")
    project_flight.draw()