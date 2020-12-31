from __future__ import annotations
from typing import List

import Line


class Point:
    def __init__(self, x, y, walls_on=None):
        if walls_on is None:
            walls_on = []
        self.x: float = x
        self.y: float = y
        self.walls_on: List[Line.Line] = walls_on
        self.seen_by: List[Point] = []

    def get_coordinates(self) -> (float, float):
        return self.x, self.y

    def __repr__(self):
        return str(self.x) + "," + str(self.y)
