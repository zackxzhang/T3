from enum import Flag


class Stone(Flag):

    _ = 0
    X = 1
    O = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


State = tuple[Stone, ...]
Board = list[list[Stone]]
Index = int
Coord = tuple[int, int]
