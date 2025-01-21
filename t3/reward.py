from .state import victorious, opponent


def victory(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    match winner:
        case ' ':
            return 0
        case stone:
            return +1
        case oppo:
            return -1
        case _:
            raise ValueError('invalid stone')

def swift_victory(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    match winner:
        case ' ':
            return -1
        case stone:
            return +10
        case oppo:
            return -10
        case _:
            raise ValueError('invalid stone')


def survival(stone: str, board: list[list], winner: str) -> int:
    oppo = opponent(stone)
    match winner:
        case ' ':
            return +1
        case stone:
            return +10
        case oppo:
            return -10
        case _:
            raise ValueError('invalid stone')
