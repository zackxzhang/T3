import itertools
from .hint import Stone, State, Board, Index, Coord


states = list(itertools.product(*[list(Stone) for _ in range(9)]))
state_0 = tuple([Stone._ for _ in range(9)])


def boardify(state: State) -> Board:
    return [list(state[0:3]), list(state[3:6]), list(state[6:9])]


def statify(board: Board) -> State:
    return (*board[0], *board[1], *board[2])


def stringify(board: Board) -> str:
    return '\n'.join(''.join(map(str, row)) for row in board)


def ij2k(ij: Coord) -> Index:
    i, j = ij
    return i * 3 + j


def k2ij(k: Index) -> Coord:
    return divmod(k, 3)


def affordance(state: State):
    for k, e in enumerate(state):
        if not e:
            yield k


def transition(state: State, k: Index, stone: Stone) -> State:
    s = list(state)
    s[k] = stone
    return tuple(s)


def victorious(stone: Stone, board: Board) -> bool:
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


def victor(board: Board) -> Stone:
    if victorious(Stone.X, board):
        return Stone.X
    if victorious(Stone.O, board):
        return Stone.O
    return Stone._


def impasse(board: Board) -> bool:
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                return False
    return True
