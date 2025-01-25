from .state import stones, victor, vectorize, full


class Arena:

    def __init__(self, rewards):
        self.rewards = rewards
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.round = 0
        self.ended = False
        self.history = list()
        self.last = None

    def __str__(self):
        return str(self.board)

    @property
    def state(self):
        return vectorize(self.board)

    def evo(self, action):
        assert not self.ended, "game is ended"
        self.history.append(action)
        stone, (i, j) = action
        assert stone != self.last
        self.last = stone
        assert self.board[i][j] == ' ', f"{i}-{j} is occupied"
        self.board[i][j] = stone
        self.round += 1
        if (winner := victor(self.board)) in stones or full(self.board):
            self.ended = True
        return self.state, [
            reward(self.board, winner=winner)
            for reward in self.rewards
        ]
