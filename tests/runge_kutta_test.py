import numpy as np

from src import RungeKutta4


g = 9.8


def function(t: list[float], y: list[float]):
    x1, x2, x3, x4 = y
    dydt = np.array([x3, x4 , 0.0, -g])
    return dydt

def surface(x: float):
    return np.cos(x)


def runge_kutta_calc_is_not_none():
    runge_kutta = RungeKutta4()
    y0 = [0.0, surface([0])[0], 7.0, 5.0]
    t = np.linspace(0, 12, 100)
    runge_kutta.run(
        f = function,
        surface = surface,
        y_start = y0,
        t = t
    )
    result1 = runge_kutta.f_result
    t1 = runge_kutta.t_result
    assert result1 is not None
    assert t1 is not None
    

def runge_kutta_calc_result_near():
    err = 0.1
    runge_kutta = RungeKutta4()
    K = 10
    m = 1
    theta = np.pi/4
    v_0 = np.sqrt(2*K/m)
    y0 = [0.0, surface(0.0), v_0*np.cos(theta), v_0*np.sin(theta)]
    t = np.linspace(0, 10, 101)
    runge_kutta.run(
        f = function,
        surface = surface,
        y_start = y0,
        t = t
    )
    result1 = runge_kutta.f_result
    t = np.linspace(0, 10, 1001)
    runge_kutta.run(
        f = function,
        surface = surface,
        y_start = y0,
        t = t
    )
    result2 = runge_kutta.f_result
    t2 = runge_kutta.t_result
    t = np.linspace(0, 10, 10001)
    runge_kutta.run(
        f = function,
        surface = surface,
        y_start = y0,
        t = t
    )
    result3 = runge_kutta.f_result
    t3 = runge_kutta.t_result
    assert np.linalg.norm(result3[300] - result1[3])/(t3[1] - t3[0])**4 < err
    assert np.linalg.norm(result3[300] - result2[30])/(t3[1] - t3[0])**4 < err


if __name__ == "__main__":
    runge_kutta_calc_is_not_none()
    runge_kutta_calc_result_near()