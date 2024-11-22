import unittest
import numpy as np

from projectile_flight import RungeKutta4


class TestUtilDate(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.g = 9.8
        self.runge_kutta = RungeKutta4()

    def __function(self, t: list[float], y: list[float]):
        try:
            x1, x2, x3, x4 = y
            dydt = np.array([x3, x4 , 0.0, -self.g])
            return dydt
        except Exception as e:
            raise Exception(f"{str(e)}. Y = {y}, t = {t}")

    def test_runge_kutta(self):
        y0 = [0.0, 0.0, 40.0, 40.0]
        t = np.linspace(0, 6, 200)
        result =  self.runge_kutta.calc(self.__function, y0, t)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)