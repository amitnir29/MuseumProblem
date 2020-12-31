from __future__ import annotations
from typing import List, Tuple, NamedTuple

import Line


class Point:
    def __init__(self, x: int, y: int, walls_on=None):
        if walls_on is None:
            walls_on = tuple()
        self.x: int = x
        self.y: int = y
        self.walls_on: Tuple[Line.Line] = walls_on

    def get_coordinates(self) -> (int, int):
        return self.x, self.y

    def __repr__(self):
        return str(self.x) + "," + str(self.y)
