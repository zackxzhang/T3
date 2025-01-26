from .hint import Stone
from .player import Player


def victory(player: Player):
    stone = player.stone
    def reward(winner: Stone) -> int:
        if winner == stone:
            return +1
        elif winner == ~stone:
            return -1
        elif not winner:
            return 0
        else:
            return 0
    return reward


def swift_victory(player: Player):
    stone = player.stone
    def reward(winner: Stone) -> int:
        if winner == stone:
            return +10
        elif winner == ~stone:
            return -10
        elif not winner:
            return -1
        else:
            return 0
    return reward


def survival(player: Player):
    stone = player.stone
    def reward(winner: Stone) -> int:
        if winner == stone:
            return +10
        elif winner == ~stone:
            return -10
        elif not winner:
            return +1
        else:
            return 0
    return reward
