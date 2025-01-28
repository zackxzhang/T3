from .struct import Stone, State
from .state import state_0, judge
from .player import Player


class Game:

    def __init__(self, players: list[Player]):
        for player in players:
            player.state = state_0
        self.players = players
        self.state = state_0
        self.round = 0
        self.winner = Stone._
        self.history: list = list()

    @property
    def player(self) -> Player:
        return self.players[self.round % 2]

    def evo(self, action: State):
        assert not self.winner, "game is ended"
        self.history.append(action)
        self.winner = judge(action)
        self.state = action
        self.round += 1
        return self.winner
