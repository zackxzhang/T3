from .struct import Stone, State
from .state import state_0, judge
from .player import Player


class Game:

    def __init__(self, players: tuple[Player, Player]):
        self.players = players
        for player in players:
            player.state = state_0
        self.round = 0
        self.winner = Stone._
        self.trajectory = [state_0]

    @property
    def player(self) -> Player:
        return self.players[self.round % 2]

    @property
    def state(self) -> State:
        return self.trajectory[-1]

    def evo(self, action: State):
        assert not self.winner, "game is ended"
        self.trajectory.append(action)
        self.winner = judge(action)
        self.round += 1
        return self.winner


class Arbiter:

    def __init__(self):
        self.wins = [0, 0, 0]

    @property
    def n(self) -> int:
        return sum(self.wins)

    def __call__(self, winner: Stone):
        if winner == Stone.X | Stone.O:
            self.wins[0] += 1
        elif winner == Stone.X:
            self.wins[1] += 1
        elif winner == Stone.O:
            self.wins[2] += 1
        else:
            raise AttributeError('no winner yet')

    def __str__(self):
        return (
            f'X {self.wins[1]/self.n}\n'
            f'- {self.wins[0]/self.n}\n'
            f'O {self.wins[2]/self.n}\n'
            '--------'
        )
