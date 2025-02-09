import functools
import itertools
from enum import Flag


class Stone(Flag):

    _ = 0
    X = 1
    O = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


Board = list[list[Stone]]
State = tuple[Stone, ...]
Index = int
Coord = tuple[int, int]


states: list[State] = list(itertools.product(
    *[(Stone._, Stone.X, Stone.O) for _ in range(9)]
))
s0 = tuple([Stone._ for _ in range(9)])


def statify(board: Board) -> State:
    return (*board[0], *board[1], *board[2])


def boardify(state: State) -> Board:
    return [list(state[0:3]), list(state[3:6]), list(state[6:9])]


def stringify(board: Board) -> str:
    return '\n'.join(''.join(map(str, row)) for row in board)


def plot(state: State) -> str:
    return stringify(boardify(state))


def affordance(state: State) -> list[Index]:
    return [k for k, e in enumerate(state) if not e]


def transition(state: State, stone: Stone, k: Index) -> State:
    s = list(state)
    s[k] = stone
    return tuple(s)


def transitions(state: State, stone: Stone) -> list[State]:
    return [transition(state, stone, k) for k in affordance(state)]


def victorious(state: State, stone: Stone) -> bool:
    board = boardify(state)
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == stone:
            return True
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == stone:
            return True
    if board[0][0] == board[1][1] == board[2][2] == stone:
        return True
    if board[2][0] == board[1][1] == board[0][2] == stone:
        return True
    return False


def impasse(state: State) -> bool:
    for s in state:
        if not s:
            return False
    return True


@functools.cache
def judge(state: State) -> Stone:
    if victorious(state, Stone.X):
        return Stone.X
    if victorious(state, Stone.O):
        return Stone.O
    if impasse(state):
        return Stone.X | Stone.O
    return Stone._
