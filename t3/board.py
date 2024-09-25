from .state import conclude


class Board:

    stones = ['x', 'o']

    def __init__(self, reward_x, reward_o):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.round = 0
        self.alive = True
        self.rewards = {'x': reward_x, 'o': reward_o}

    def __str__(self):
        return str(self.board)

    @property
    def stone(self):
        return self.stones[self.round % 2]

    def transit(self, i, j):
        assert self.alive
        assert self.board[i][j] == ' '
        self.board[i][j] = stone
        if conclude(self.board, self.stone):
            self.alive = False
        else:
            self.round += 1
        return self.rewards[self.stone](self.board)
