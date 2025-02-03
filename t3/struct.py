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
Value = dict[State, float]


Index = int
Coord = tuple[int, int]


def ij2k(ij: Coord) -> Index:
    i, j = ij
    return i * 3 + j


def k2ij(k: Index) -> Coord:
    return divmod(k, 3)


class Mode(Flag):

    EXPLORE = 1
    EXPLOIT = 2
