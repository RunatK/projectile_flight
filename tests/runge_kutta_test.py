import numpy as np

from src.cauchy_solution import RungeKutta4


g = 9.8


def function(t: list[float], y: list[float]):
    x1, x2, x3, x4 = y
    dydt = np.array([x3, x4 , 0.0, -g])
    return dydt

def surface(x: float):
    return 0


def runge_kutta_calc_is_not_none():
    runge_kutta = RungeKutta4()
    y0 = [0.0, surface(0), 7.0, 5.0]
    t = 0
    runge_kutta.run(
        f = function,
        surface = surface,
        y_start = y0,
        t_start = t,
        h = 10**(-3)
    )
    result1 = runge_kutta.f_result
    t1 = runge_kutta.t_result
    assert result1 is not None
    assert t1 is not None
    

def runge_kutta_calc_result_near():
    err = 10**(-2)
    runge_kutta = RungeKutta4()
    K = 10
    m = 1
    theta = np.pi/4
    v_0 = np.sqrt(2*K/m)
    y0 = [0.0, surface(0.0), v_0*np.cos(theta), v_0*np.sin(theta)]
    t = 0
    for pow in range(2, 5):
        runge_kutta.run(function, surface, y0, t, h=10**(-pow))
        f_result_1 = runge_kutta.f_result
        t_result_1 = runge_kutta.t_result
        runge_kutta.run(function, surface, y0, t, h=10**(-pow-1))
        f_result_2 = runge_kutta.f_result
        t_result_2 = runge_kutta.t_result
        max_error = 0
        f_result_2_len = len(f_result_2)
        for i in range(len(f_result_1)):
            if i * 10 >= f_result_2_len:
                break
            max_error = max(max_error, abs(f_result_1[i][1] - f_result_2[i*10][1]))
        assert max_error < err

def runge_kutta_test():
    err = 10**(-2)
    runge_kutta = RungeKutta4()
    K = 10
    m = 1
    theta = np.pi/4
    v_0 = np.sqrt(2*K/m)
    y0 = [0.0, surface(0.0), v_0*np.cos(theta), v_0*np.sin(theta)]
    t = np.linspace(0, 10, 51)
    runge_kutta.k4_test(function, y0, t)
    f_result_1 = runge_kutta.f_result
    t_result_1 = runge_kutta.t_result
    t = np.linspace(0, 10, 501)
    runge_kutta.k4_test(function, y0, t)
    f_result_2 = runge_kutta.f_result
    t_result_2 = runge_kutta.t_result
    t = np.linspace(0, 10, 5001)
    runge_kutta.k4_test(function, y0, t)
    f_result_3 = runge_kutta.f_result
    t_result_3 = runge_kutta.t_result
    assert np.linalg.norm(f_result_3[-1] - f_result_1[-1])/(t_result_1[1] - t_result_1[0])**4 < err
    assert np.linalg.norm(f_result_3[-1] - f_result_2[-1])/(t_result_2[1] - t_result_2[0])**4 < err
