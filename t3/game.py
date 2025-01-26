from .state import Stone, state_0, boardify, statify, stringify, victor, impasse


class Game:

    def __init__(self, players, reward_functions):
        for player in players:
            player.state = state_0
        self.board = boardify(state_0)
        self.round = 0
        self.winner = Stone._
        self.history = list()
        self.prev = players[1].stone
        self.reward_functions = reward_functions

    def __str__(self):
        return stringify(self.board)

    @property
    def state(self):
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
        return [rf(self.winner) for rf in self.reward_functions]
