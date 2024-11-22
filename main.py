import numpy as np

from projectile_flight.runge_kutta import RungeKutta4


g = 9.8


def function(t: list[float], y: list[float]):
    try:
        x1, x2, x3, x4 = y
        dydt = np.array([x3, x4 , 0.0, -g])
        return dydt
    except Exception as e:
        raise Exception(f"{str(e)}. Y = {y}, t = {t}")



if __name__ == "__main__":
    runge_kutta = RungeKutta4()
    y0 = [0.0, 0.0, 40.0, 40.0]
    t = np.linspace(0, 6, 200)
    result =  runge_kutta.calc(function, y0, t)
    