from typing import Callable, Iterable
from abc import ABC, abstractmethod

from matplotlib import pyplot as plt
import numpy as np

from .interpolation.hermite_polynomial import HermitePolynomial
from .cauchy_solution.runge_kutta import RungeKutta4
from .iterations_method.method_chord import ChordMethod


class ProjectileFlightBase(ABC):
    def __init__(self, surface: Callable[[float], float], error: float = 10**(-8)):
        self.surface = surface
        self.runge_kutta = RungeKutta4()
        self.t_between: tuple[float, float] | None = None
        self.point_1_x1: tuple[float, float, float, float] | None = None
        self.point_2_x1: tuple[float, float, float, float] | None = None
        self.point_1_x2: tuple[float, float, float, float] | None = None
        self.point_2_x2: tuple[float, float, float, float] | None = None
    
    def _set_touch_cut(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            surface: Callable[[Iterable[float]], Iterable[float]],
            y_start: Iterable[float], 
            t_start: float,
            h: float = 10**(-2)
        ) -> None:
        self.runge_kutta.run(
            f = f,
            surface = surface,
            y_start = y_start,
            t_start = t_start,
            h = h
        )
        rk_result = self.runge_kutta.f_result
        t = self.runge_kutta.t_result
        self.t_between = (t[-2], t[-1])
        self.point_1_x1 = (t[-2], rk_result[-2][0], rk_result[-2][2])
        self.point_2_x1 = (t[-1] , rk_result[-1][0], rk_result[-1][2])
        self.point_1_x2 = (t[-2], rk_result[-2][1], rk_result[-2][2])
        self.point_2_x2 = (t[-1] , rk_result[-1][1], rk_result[-1][3])

    @abstractmethod
    def draw(self):
        t = np.linspace(self.t_between[0], self.t_between[1], 10)
        plt.plot(self.runge_kutta.f_result[:, 0], self.runge_kutta.f_result[:, 1], 'g', label='Полет снаряда')
        plt.plot(self.runge_kutta.f_result[:, 0], self.surface(self.runge_kutta.f_result[:, 0]), 'b', label='Плоскость')
        plt.plot(list(map(self.get_polynomial_value_x1, t)), list(map(self.get_polynomial_value_x2, t)), 'r', label='Эрмит')
        plt.legend(loc='best')
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.show()
