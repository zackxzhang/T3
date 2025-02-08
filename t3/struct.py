from enum import Flag


class Stone(Flag):

    _ = 0
    X = 1
    O = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Mode(Flag):

    EXPLORE = 1
    EXPLOIT = 2


Board = list[list[Stone]]
State = tuple[Stone, ...]
Value = dict[State, float]

Index = int
Coord = tuple[int, int]
