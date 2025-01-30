from abc import ABC, abstractmethod
from math import pi, cos


class Schedule(ABC):

    @property
    def t(self):
        return self._t

    @property
    def a(self):
        return self._a

    @abstractmethod
    def step(self):
        pass

    def __call__(self):
        self.step()
        return self.a


class LinearSchedule(Schedule):

    def __init__(self, t_max, a_max, a_min):
        self.d = (a_max - a_min) / t_max
        self._a = a_max + self.d
        self._t = -1

    def step(self):
        self._t += 1
        self._a -= self.d


class CosineSchedule(Schedule):

    def __init__(self, t_max, a_max, a_min):
        self._t = -1
        self.T = t_max
        self.b = a_min
        self.c = 0.5 * (a_max - a_min)

    def step(self):
        self._t += 1
        self._a = self.b + self.c * (1 + cos(pi * self.t / self.T))


class ExponentialSchedule(Schedule):

    def __init__(self, t_max, a_max, a_min, gamma):
        self.g = gamma
        self.d = 1 / gamma
        self.b = a_min
        self.c = a_max - a_min
        self._t = -1

    def step(self):
        self._t += 1
        self.d *= self.g
        self._a = self.b + self.c * self.d


class MCTS:
    """monte carlo tree search"""
