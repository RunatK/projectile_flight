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
            t_start: float,
            h: float = 10**(-3)
        ) -> bool:
            return self.__k4(
                f = f,
                surface = surface,
                y_start = y_start,
                t_start = t_start,
                h = h
            )
    
    def __k4(
            self,
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            surface: Callable[[float], Iterable[float]],
            y_start: Iterable[float], 
            t_start: float,
            h: float
        ) -> bool:
        """
        Get values of the f in the points. Before f value in the point not more then value in the surface.
        """
        t: list[float] = [t_start]
        self.f_result = [y_start]
        flag = True
        counter = 0
        while flag:
            t.append(t[counter] + h)
            k1 = f(t[counter], self.f_result[counter])
            k2 = f(t[counter]+h/2., self.f_result[counter]+k1*h/2.)
            k3 = f(t[counter]+h/2., self.f_result[counter]+k2*h/2.)
            k4 = f(t[counter]+h, self.f_result[counter]+k3*h)
            self.f_result.append(self.f_result[counter] + (k1 + 2 * k2 + 2 * k3 + k4)*(h / 6.))
            if self.f_result[counter][1] < surface(self.f_result[counter][0]):
                self.f_result = np.array(self.f_result[:counter+1])
                self.t_result = np.array(t[:counter+1])
                flag = False
            counter += 1
        return flag