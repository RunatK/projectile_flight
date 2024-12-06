from typing import Callable


class ChordMethod:
    def __init__(self, error: float):
        self.error = error
        self.max_iter = 10000
    
    def run(self, start: float, end: float , f: Callable[[float], float]):
        x_start = start
        x_end = end
        counter = 0
        while counter < self.max_iter:
            f_start = f(x_start)
            f_end = f(x_end)
            x_next = x_start - (x_end - x_start) * f_start / (f_end - f_start)
            x_start = x_end
            x_end = x_next
            counter += 1
            if abs(f(x_next)) < self.error:
                return x_next
        raise RuntimeError("The chord method does not converge")