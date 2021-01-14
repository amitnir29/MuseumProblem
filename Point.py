from __future__ import annotations

from typing import Tuple

import Line


class Point:
    def __init__(self, x: int, y: int, walls_on=None):
        if walls_on is None:
            walls_on = tuple()
        self.x: int = x
        self.y: int = y
        self.walls_on: Tuple[Line.Line] = walls_on

    def get_coordinates(self) -> (int, int):
        """
        :return: return the (x,y) values of the point
        """
        return self.x, self.y

    def __repr__(self):
        """
        :return: a representation form of the point
        """
        return str(self.x) + "," + str(self.y)

    def add_coordinates(self, coor: Tuple) -> Point:
        """
        :param coor: coordinates to add to the point (x,y)
        :return: the new point
        """
        return Point(self.x + coor[0], self.y + coor[1])

    def __eq__(self, other: Point):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.walls_on)
