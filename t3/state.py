import itertools


states = itertools.product(*[[' ', 'x', 'o'] for _ in range(9)])


def matrixify(state: list) -> list[list]:
    return [state[0:3], state[3:6], state[6:9]]


def linearize(board: list[list]) -> list:
    return [*board[0], *board[1], *board[2]]


def stringify(state: list) -> str:
    return ''.join(state)


def vectorize(string: str) -> list:
    return list(string)


def actions(state: list):
    for i, e in enumerate(state):
        if e == ' ':
            yield i


def conclude(board: list[list], stone: str) -> bool:
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
