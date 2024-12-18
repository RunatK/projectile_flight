from typing import Callable

import numpy as np


class RungeKutta4:
    def calc(
            self, 
            f: Callable[[list[float], list[float]], list[float]], 
            y_start: list[float], 
            t: list[float]
        ) -> list[float]:
        """
        Get values of the f in the points
        """
        n = len(t)
        result = np.zeros((n, len(y_start)))
        result[0] = y_start
        for i in range(n-1):
            h = t[i+1] - t[i]
            k1_1 = h*f(t[i], result[i])
            k1_2 = h*f(t[i]+h/2., result[i]+k1_1*h/2.)
            k1_3 = h*f(t[i]+h/2., result[i]+k1_2*h/2.)
            k1_4 = h*f(t[i]+h, result[i]+k1_3*h)
            result[i+1] = result[i] + (k1_1 + 2*k1_2 + 2*k1_3 + k1_4)/6.*h
        return result
