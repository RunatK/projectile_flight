from typing import Iterable


class HermitePolynomial:
    def run(self, t: Iterable[float], point_1: tuple[float, float, float], point_2: tuple[float, float, float]):
        t1, x1, dx1 = point_1
        t2, x2, dx2 = point_2
        x_min = (t - t1)/(t2 - t1)
        return self.__h_00(x_min) * x1 + self.__h_10(x_min) * (t2 - t1) * dx1 + self.__h_01(x_min) * x2 + self.__h_11(x_min) * (t2 - t1) * dx2

    def __h_00(self, t):
        return 2*t**3 - 3*t**2 + 1
    
    def __h_10(self, t):
        return t**3 - 2*t**2 + t
    
    def __h_01(self, t):
        return -2*t**3 + 3*t**2
    
    def __h_11(self, t):
        return t**3 - t**2