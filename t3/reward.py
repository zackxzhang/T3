from .state import victorious, opponent


def victory(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    if winner == ' ':
        return 0
    elif winner == stone:
        return +1
    elif winner == oppo:
        return -1
    else:
        raise ValueError('invalid stone')


def swift_victory(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    if winner == ' ':
        return -1
    elif winner == stone:
        return +10
    elif winner == oppo:
        return -10
    else:
        raise ValueError('invalid stone')


def survival(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    if winner == ' ':
        return +1
    elif winner == stone:
        return +10
    elif winner == oppo:
        return -10
    else:
        raise ValueError('invalid stone')
