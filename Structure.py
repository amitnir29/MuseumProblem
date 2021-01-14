from __future__ import annotations

from collections import defaultdict
from typing import List, Dict, Tuple, FrozenSet, Optional

from Point import Point


class Square:
    def __init__(self, points: Tuple[Point, Point, Point, Point]):
        self.points: Tuple[Point, Point, Point, Point] = points
        self.are_connected: Dict[FrozenSet[Point, Point], Square] = dict()
        self.structure: Optional[Structure] = None
        self.create_connected_dict()

    def get_neighbors(self, point: Point) -> Optional[Tuple[Point, Point]]:
        """
        :param point: input point
        :return: the neighbor points of the input point in the square
        """
        if point not in self.points:
            return None
        index = self.points.index(point)
        # return the prev and next points
        return self.points[index - 1], self.points[(index + 1) % 4]

    def get_connected_value(self, p1, p2) -> Optional[Square]:
        """
        getter for a points pair in the dict
        :param p1: one point
        :param p2: second point
        :return: the value of the pair in the dict, None if not in the dict
        """
        pair = frozenset((p1, p2))
        if pair not in self.are_connected:
            return None
        return self.are_connected[pair]

    def set_connected_value(self, p1, p2, value: Optional[Square]):
        """
        setter for a points pair in the dict
        :param p1: one point
        :param p2: second point
        :param value: new value for the pair in the dict
        """
        self.are_connected[frozenset((p1, p2))] = value
        # check if after update we have more connected lines than max allowed
        if self.structure is None:
            return
        if self not in self.structure.available_squares:
            return
        if len([k for k in self.are_connected if self.are_connected[k] is not None]) > \
                self.structure.max_occupied_lines:
            # we should remove the square from the structure's list of available_squares
            index = self.structure.available_squares.index(self)
            self.structure.available_squares.pop(index)

    def create_connected_dict(self) -> None:
        """
        create the dict of the square
        """
        for i in range(len(self.points)):
            self.set_connected_value(self.points[i], self.points[i - 1], None)


class Structure:
    def __init__(self, more_unified=True):
        self.squares: List[Square] = list()
        self.max_occupied_lines: int = 3 if more_unified else 2
        self.available_squares: List[Square] = list()

    def append(self, square: Square):
        """
        add the square to the list of squares
        :param square: a new square
        """
        self.squares.append(square)
        if len([k for k in square.are_connected if square.are_connected[k] is not None]) <= self.max_occupied_lines:
            self.available_squares.append(square)
        square.structure = self

    def get_all_points(self) -> Dict[Point, List[Square]]:
        """
        :return: a dict from each point to the squares it is on
        """
        results: Dict[Point, List[Square]] = defaultdict(list)
        for square in self.squares:
            for p in square.points:
                results[p].append(square)
        return results
