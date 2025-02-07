from abc import ABC, abstractmethod
from .struct import Stone


class Reward(ABC):

    def __init__(self, stone: Stone):
        self.stone = stone

    @abstractmethod
    def __call__(self, winner: Stone):
        pass


class Victory(Reward):

    name = 'victory'

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

    name = 'swift-victory'

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

    name = 'survival'

    def __call__(self, winner: Stone) -> int:
        if winner == self.stone:
            return +10
        elif winner == ~self.stone:
            return -10
        elif not winner:
            return +1
        else:
            return 0


def decode_reward(name: str) -> type[Reward]:
    match name:
        case 'victory':
            return Victory
        case 'swift-victory':
            return SwiftVictory
        case 'survival':
            return Survival
        case _:
            raise ValueError(f'no reward function named {name}')
