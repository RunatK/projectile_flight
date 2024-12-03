import unittest

from matplotlib import pyplot as plt
import numpy as np

from src import RungeKutta4


def function(t: list[float], y: list[float]):
    g = 9.8
    try:
        x1, x2, x3, x4 = y
        dydt = np.array([x3, x4 , 0.0, -g])
        return dydt
    except Exception as e:
        raise Exception(f"{str(e)}. Y = {y}, t = {t}")


def surface(x: list[float]):
    return np.cos(x)


class TestDataSummary(unittest.TestCase):
    def runge_kutta_calc(self):
        runge_kutta = RungeKutta4()
        y0 = [0.0, surface([0])[0], 7.0, 5.0]
        t = np.linspace(0, 12, 100)
        result = runge_kutta.calc(function, y0, t)
        print(result)
        x1 = [i[0] for i in result]
        x2 = [i[1] for i in result]
        self.assertIsNotNone(x1)
        self.assertIsNotNone(x2)
        plt.plot(x1, x2)
        plt.plot(t, surface(t))
        plt.show()


if __name__ == '__main__':
    unittest.main()