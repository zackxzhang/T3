from .state import state_0, boardify, statify, stringify, victor, impasse
from .player import Player
from .hint import Stone, State


class Game:

    def __init__(self, players: list[Player]):
        for player in players:
            player.state = state_0
        self.players = players
        self.board = boardify(state_0)
        self.prev = players[1].stone
        self.round = 0
        self.winner = Stone._
        self.history: list = list()

    def __str__(self) -> str:
        return stringify(self.board)

    @property
    def player(self) -> Player:
        return self.players[self.round % 2]

    @property
    def state(self) -> State:
        return statify(self.board)

    def evo(self, action):
        assert not self.winner, "game is ended"
        self.history.append(action)
        stone, (i, j) = action
        assert self.prev == ~stone
        self.prev = stone
        assert not self.board[i][j], f"{i}-{j} is occupied"
        self.board[i][j] = stone
        self.round += 1
        self.winner = victor(self.board)
        if impasse(self.board):
            self.winner = Stone.X | Stone.O
        return self.winner
