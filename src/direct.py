from typing import Callable, Iterable

from matplotlib import pyplot as plt
import numpy as np

from .interpolation.hermite_polynomial import HermitePolynomial
from .cauchy_solution.runge_kutta import RungeKutta4
from .iterations_method.method_secant import SecantMethod


class ProjectileFlightDirect:
    def __init__(self, surface: Callable[[float], float], error: float = 10**(-4)):
        self.polynamial = HermitePolynomial()
        self.runge_kutta = RungeKutta4()
        self.chord_method = SecantMethod(error)
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
            t_start: float,
            h: float = 10**(-2)
        ) -> float:
        """
        Get projectile landing time and set runge kutta points for working with interpolation polynom
        """
        self.__set_touch_cut(f, self.surface, y_start, t_start, h)
        return self.chord_method.run(
            start = self.t_between[0],
            end = self.t_between[1],
            f = self.__surface_distance
        )

    def __set_touch_cut(
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
        self.point_1_x2 = (t[-2], rk_result[-2][1], rk_result[-2][3])
        self.point_2_x2 = (t[-1] , rk_result[-1][1], rk_result[-1][3])

    def __surface_distance(self, t: float):
        return self.get_polynomial_value_x2(t) - self.surface(self.get_polynomial_value_x1(t))
    
    def get_polynomial_value_x2(self, t: float | Iterable[float]):
        if self.t_between[0] > t  or t > self.t_between[1]:
            raise ValueError(f"t must be between {self.t_between[0]} and {self.t_between[1]}. t value: {t}")
        return self.polynamial.run(t, self.point_1_x2, self.point_2_x2)
    
    def get_polynomial_value_x1(self, t: float | Iterable[float]):
        if t is Iterable and (self.t_between[0] > t  or t > self.t_between[1]):
            raise ValueError(f"t must be between {self.t_between[0]} and {self.t_between[1]}. t value: {t}")
        return self.polynamial.run(t, self.point_1_x1, self.point_2_x1)
    
    def draw(self, t: float):
        t_hermit = np.linspace(self.t_between[0], self.t_between[1], 10)
        x_1 = self.get_polynomial_value_x1(t)
        x_2 = self.get_polynomial_value_x2(t)
        plt.plot(self.runge_kutta.f_result[:, 0], self.runge_kutta.f_result[:, 1], 'g', label='Полет снаряда')
        plt.plot(self.runge_kutta.f_result[:, 0], self.surface(self.runge_kutta.f_result[:, 0]), 'b', label='Плоскость')
        plt.plot(list(map(self.get_polynomial_value_x1, t_hermit)), list(map(self.get_polynomial_value_x2, t_hermit)), 'r', label='Эрмит')
        plt.plot(x_1, x_2, 'ro', color='y', label='Решение')
        plt.legend(loc='best')
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.show()
