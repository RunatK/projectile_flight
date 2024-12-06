from typing import Callable, Iterable

import numpy as np


class RungeKutta4:
    @property
    def f_result(self) -> np.ndarray:
        return self._f_result
    
    @f_result.setter
    def f_result(self, value: np.ndarray):
        self._f_result = value

    @property
    def t_result(self) -> list[float]:
        return self._t_result
    
    @t_result.setter
    def t_result(self, value: list[float]):
        self._t_result = value
    
    def run(
            self,
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            surface: Callable[[Iterable[float]], Iterable[float]],
            y_start: Iterable[float], 
            t: Iterable[float] = None,
            n: int = None
        ) -> None:
        if isinstance(t, Iterable):
            return self.__k4(
                f = f,
                surface = surface,
                y_start = y_start,
                t = t
            )
        elif t is None:
            t = self.get_t(n)
    
    def __k4(
            self,
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            surface: Callable[[float], Iterable[float]],
            y_start: Iterable[float], 
            t: list[float]
        ) -> Iterable[float]:
        """
        Get values of the f in the points. Before f value in the point not more then value in the surface.
        """
        n = len(t)
        self.f_result = np.zeros((n, len(y_start)))
        self.f_result[0] = y_start
        for i in range(n-1):
            h = t[i+1] - t[i]
            k1 = f(t[i], self.f_result[i])
            k2 = f(t[i]+h/2., self.f_result[i]+k1*h/2.)
            k3 = f(t[i]+h/2., self.f_result[i]+k2*h/2.)
            k4 = f(t[i]+h, self.f_result[i]+k3*h)
            self.f_result[i+1] = self.f_result[i] + (k1 + 2 * k2 + 2 * k3 + k4)*(h / 6.)
            if self.f_result[i][1] < surface(self.f_result[i][0]):
                self.f_result = self.f_result[:i+1]
                self.t_result = t[:i+1]
                return
        raise RuntimeError("There are not any concat point. You can increase the size of t")

    def get_t(self, n: int) -> Iterable[float]:
        return np.linspace(0, 12, 100)
