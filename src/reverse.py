from typing import Callable, Iterable, Generator

from matplotlib import pyplot as plt
import numpy as np

from .iterations_method.method_secant import SecantMethod
from .direct import ProjectileFlightDirect
from .dto.theta_interval import ThetaInterval


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
        self.max_iter = 50
        self.chord_method = SecantMethod(error, max_iter = 50)
        self.direct = ProjectileFlightDirect(surface, error)

    def run(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]],
            t_start: float,
            x_1: float,
            h: float = 10**(-3)
        ) -> float:
        thetas = np.linspace(0, np.pi/2, 90)
        thetas_results = [(result[2], result[0]) for result in self._run_thetas_calc(f, t_start, thetas, h)]
        # thetas_results = np.array(thetas_results)
        # plt.scatter(thetas_results[:, 1], thetas_results[:, 0], s=0.9)
        # plt.xlabel('theta')
        # plt.ylabel('x1')
        # plt.show()
        results = []
        for interval in self.__get_interval_with_x_1(thetas_results, x_1):
            result = self.chord_method.run(
                start = interval.theta1,
                end = interval.theta2,
                f = lambda x: self._direct_run(f, t_start, x, h)[2] - x_1
            )
            results.append(result)
        return results

        
    def _run_thetas_calc(
        self, 
        f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
        t_start: float,
        thetas: list[float],
        h: float = 10**(-2)  
    ) -> Generator[tuple[float, float, float], None, None]:
        for theta in thetas:
            yield self._direct_run(
                f = f,
                t_start = t_start,
                theta = theta,
                h = h
            )
    
    def  _direct_run(
        self, 
        f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
        t_start: float,
        theta: float,
        h: float = 10**(-2)
    ) -> tuple[float, float, float]:
        y_start = self.get_y_0(theta)
        t = self.direct.run(
            f = f,
            y_start = y_start,
            t_start = t_start,
            h = h
        )
        return (theta, t, self.direct.get_polynomial_value_x1(t), self.direct.get_polynomial_value_x2(t))
        

    def __get_interval_with_x_1(self, theta_x1: list[tuple[float, float]], x_1: float) -> Generator[ThetaInterval, None, None]:
        for i in range(len(theta_x1)-1):
            if theta_x1[i][0] < x_1 < theta_x1[i+1][0]:
                yield ThetaInterval(
                    theta1 = theta_x1[i][1],
                    theta2 = theta_x1[i+1][1]
                )
            if theta_x1[i-1][0] > x_1 > theta_x1[i][0]:
                yield ThetaInterval(
                    theta1 = theta_x1[i-1][1],
                    theta2 = theta_x1[i][1]
                )

    def get_y_0(self, theta: float) -> tuple[float, float, float, float]:
        return (0.0, self.surface(0.0), self.v_0*np.cos(theta), self.v_0*np.sin(theta))
    
    def draw(
            self, 
            f: Callable[[Iterable[float], Iterable[float]], Iterable[float]], 
            t_start: float,
            thetas: list[float],
            h: float = 10**(-2)
        ):
        for theta in thetas:
            y_start = self.get_y_0(theta)
            t = self.direct.run(
                f = f,
                y_start = y_start,
                t_start = t_start,
                h = h
            )
            plt.plot(self.direct.runge_kutta.f_result[:, 0], self.direct.runge_kutta.f_result[:, 1], 'g', label=f'Полет снаряда {theta}')
        plt.plot(self.direct.runge_kutta.f_result[:, 0], self.surface(self.direct.runge_kutta.f_result[:, 0]), 'b', label='Плоскость')
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.show()
