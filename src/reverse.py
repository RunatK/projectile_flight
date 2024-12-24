from typing import Callable, Iterable, Generator

from matplotlib import pyplot as plt
import numpy as np

from .interpolation.hermite_polynomial import HermitePolynomial
from .cauchy_solution.runge_kutta import RungeKutta4
from .iterations_method.method_chord import ChordMethod
from .direct import ProjectileFlightDirect


class ProjectileFlightReverse:
    def __init__(
            self, 
            surface: Callable[[float], float],
            v_0: float = None,
            error: float = 10**(-4)
        ):
        self.surface = surface
        if v_0 is None:
            k = 100
            m = 1
            self.v_0 = np.sqrt(2*k/m)
        else:
            self.v_0 = v_0
        self.polynamial = HermitePolynomial()
        self.runge_kutta = RungeKutta4()
        self.chord_method = ChordMethod(error)
        self.direct = ProjectileFlightDirect(surface, error)

    def run(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]],
            t_start: float,
            h: float = 10**(-2)
        ) -> float:
        thetas = np.linspace(0, np.pi/2, 90)
        results = [result for result in self._run(f, t_start, thetas, h)]
        results = np.array(results)
        plt.scatter(results[:, 1], results[:, 0], s=0.9)
        plt.xlabel('theta')
        plt.ylabel('x1')
        plt.show()
        
    def _run(
        self, 
        f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
        t_start: float,
        thetas: float,
        h: float = 10**(-2)  
    ) -> Generator[float, None, None]:
            for theta in thetas:
                print(theta)
                y_start = self.get_y_0(theta)
                t = self.direct.run(
                    f = f,
                    y_start = y_start,
                    t_start = t_start,
                    h = h
                )
                yield (t, self.direct.get_polynomial_value_x1(t), self.direct.get_polynomial_value_x2(t))

    def get_y_0(self, theta: float) -> tuple[float, float, float, float]:
        return (0.0, self.surface(0.0), self.v_0*np.cos(theta), self.v_0*np.sin(theta))
    
    def draw(self):
        t = np.linspace(self.t_between[0], self.t_between[1], 10)
        plt.plot(self.runge_kutta.f_result[:, 0], self.runge_kutta.f_result[:, 1], 'g', label='Полет снаряда')
        plt.plot(self.runge_kutta.f_result[:, 0], self.surface(self.runge_kutta.f_result[:, 0]), 'b', label='Плоскость')
        plt.plot(list(map(self.get_polynomial_value_x1, t)), list(map(self.get_polynomial_value_x2, t)), 'r', label='Эрмит')
        plt.legend(loc='best')
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.show()
