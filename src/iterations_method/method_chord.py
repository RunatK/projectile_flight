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
            if f_start == f_end:
                return x_next
            x_next = x_start - (x_end - x_start) * f_start / (f_end - f_start)
            x_start = x_end
            x_end = x_next
            counter += 1
            distance = abs(f(x_next))
            if distance < self.error:
                return x_next
            print(f"Chord method iteration: {counter}. Distance: {distance}. Value: {x_next}")
        raise RuntimeError("The chord method does not converge")