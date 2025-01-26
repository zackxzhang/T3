from abc import ABC, abstractmethod
from .hint import Stone


class Reward(ABC):

    def __init__(self, stone: Stone):
        self.stone = stone

    @abstractmethod
    def __call__(self, winner: Stone):
        ...


class Victory(Reward):

    def __call__(self, winner: Stone) -> int:
        if winner == self.stone:
            return +1
        elif winner == ~self.stone:
            return -1
        elif not winner:
            return 0
        else:
            return 0


class SwiftVictory(Reward):

    def __call__(self, winner: Stone) -> int:
        if winner == self.stone:
            return +10
        elif winner == ~self.stone:
            return -10
        elif not winner:
            return -1
        else:
            return 0


class Survival(Reward):

    def __call__(self, winner: Stone) -> int:
        if winner == self.stone:
            return +10
        elif winner == ~self.stone:
            return -10
        elif not winner:
            return +1
        else:
            return 0
