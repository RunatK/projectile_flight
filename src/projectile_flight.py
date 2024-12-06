from typing import Callable, Iterable

import numpy as np

from .hermite_polynomial import HermitePolynomial
from .runge_kutta import RungeKutta4
from .method_chord import ChordMethod


class ProjectileFlight:
    def __init__(self, surface: Callable[[float], float], h: float):
        error = h**4
        self.polynamial = HermitePolynomial()
        self.runge_kutta = RungeKutta4()
        self.chord_method = ChordMethod(error)
        self.parts = 10
        self.surface = surface
        self.t_between: tuple[float, float] | None = None
        self.point_1_x1: tuple[float, float, float, float] | None = None
        self.point_2_x1: tuple[float, float, float, float] | None = None
        self.point_1_x2: tuple[float, float, float, float] | None = None
        self.point_2_x2: tuple[float, float, float, float] | None = None

    def run(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            y_start: Iterable[float], 
            t: Iterable[float] = None,
            n: int = None
        ):
        self.set_touch_cut(f, self.surface, y_start, t, n)
        return self.chord_method.run(
            start = self.t_between[0],
            end = self.t_between[1],
            f = self.__surface_distance
        )

    def set_touch_cut(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            surface: Callable[[Iterable[float]], Iterable[float]],
            y_start: Iterable[float], 
            t: Iterable[float] = None,
            n: int = None
        ) -> None:
        self.runge_kutta.run(
            f = f,
            surface = surface,
            y_start = y_start,
            t = t,
            n = n
        )
        rk_result = self.runge_kutta.f_result
        t = self.runge_kutta.t_result
        self.t_between = (t[-2], t[-1])
        self.point_1_x1 = (t[-2], rk_result[-2][0], rk_result[-2][2])
        self.point_2_x1 = (t[-1] , rk_result[-1][0], rk_result[-1][2])
        self.point_1_x2 = (t[-2], rk_result[-2][1], rk_result[-2][2])
        self.point_2_x2 = (t[-1] , rk_result[-1][1], rk_result[-1][3])

    def __surface_distance(self, t: float):
        return self.get_polynomial_value_x2(t) - self.surface(self.get_polynomial_value_x1(t))
    
    def get_polynomial_value_x2(self, t: float):
        if self.t_between[0] > t  or t > self.t_between[1]:
            raise ValueError(f"t must be between {self.t_between[0]} and {self.t_between[1]}. t value: {t}")
        return self.polynamial.run(t, self.point_1_x2, self.point_2_x2)
    
    def get_polynomial_value_x1(self, t: float):
        if self.t_between[0] > t  or t > self.t_between[1]:
            raise ValueError(f"t must be between {self.t_between[0]} and {self.t_between[1]}. t value: {t}")
        return self.polynamial.run(t, self.point_1_x1, self.point_2_x1)
