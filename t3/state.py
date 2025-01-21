import itertools
from .hint import State, Board


stones = ['x', 'o']
states = itertools.product(*[[' ', 'x', 'o'] for _ in range(9)])


def opponent(stone: str) -> str:
    match stone:
        case 'x':
            return 'o'
        case 'o':
            return 'x'
        case _:
            raise ValueError('invalid stone')


def matricize(state: State) -> Board:
    return [list(state[0:3]), list(state[3:6]), list(state[6:9])]


def vectorize(board: Board) -> State:
    return (*board[0], *board[1], *board[2])


def stringify(state: State) -> str:
    return ''.join(state)


def tuplify(string: str) -> State:
    return tuple(string)


def ij2k(i: int, j: int):
    return i * 3 + j


def k2ij(k: int) -> tuple[int, int]:
    return divmod(k, 3)


def affordance(state: State):
    for k, e in enumerate(state):
        if e == ' ':
            yield k


def transition(state: State, k: int, stone: str):
    s = list(state)
    s[k] = stone
    return tuple(s)


def victorious(stone: str, board: Board) -> bool:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == stone:
            return True
    for j in range(3):
        if board[i][0] == board[i][1] == board[i][2] == stone:
            return True
    if board[0][0] == board[1][1] == board[2][2] == stone:
        return True
    if board[2][0] == board[1][1] == board[0][2] == stone:
        return True
    return False


def victor(board: Board) -> str:
    for stone in stones:
        if victorious(stone, board):
            return stone
    return ' '
