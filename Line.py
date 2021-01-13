from __future__ import annotations

from typing import Optional

from Point import Point
from math import inf

epsilon = 1e-6


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1: Point = p1
        self.p2: Point = p2

    def slope(self) -> float:
        """
        :return: slope of the line
        """
        if self.p1.x == self.p2.x:
            return inf
        return (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)

    def get_mb(self) -> (float, float):
        """
        :return: m,b values for the line equation, such that y=mx+b
        """
        s = self.slope()
        return s, (self.p1.y - s * self.p1.x)

    def is_in_y_range(self, y: float):
        """
        :param y: input y value
        :return: True if y is between the min y and max y of the line
        """
        return min(self.p1.y, self.p2.y) - epsilon <= y <= max(self.p1.y, self.p2.y) + epsilon

    def is_in_x_range(self, x: float):
        """
        :param x: input y value
        :return: True if x is between the min x and max x of the line
        """
        return min(self.p1.x, self.p2.x) - epsilon <= x <= max(self.p1.x, self.p2.x) + epsilon

    def is_in_range(self, x: float, y: float):
        """
        :param x: input x value
        :param y: input y value
        :return: True if the point represented by (x,y) is in the range of the line
        """
        return self.is_in_x_range(x) and self.is_in_y_range(y)

    def contains_point(self, p: Point):
        """
        :param p: a point
        :return: True if the point is on the line
        """
        if not self.is_in_range(p.x, p.y):
            return False
        if self.slope() == inf:
            return True
        m, b = self.get_mb()
        return p.y == m * p.x + b

    def is_intersecting(self, other: Line) -> bool:
        """
        :param other: another line
        :return: True if the lines intersect
        """
        if self.slope() == other.slope():
            # they are parallel, so they are either no connected at all, or have a certain overlap
            return self.contains_point(other.p1) or self.contains_point(other.p2) \
                   or other.contains_point(self.p1) or other.contains_point(self.p2)
        # else, they are not parallel, they either intersect in a single point, or do not intersect
        # get the m,b of the lines
        m1, b1 = self.get_mb()
        m2, b2 = other.get_mb()
        # if self is parallel to the y axis. we know other is for sure not, because they are not parallel
        if m1 == inf:
            # get the y of the other line at the x value of the inf line
            line1_x = self.p1.x
            inter_y = m2 * line1_x + b2
            return self.is_in_range(line1_x, inter_y) and other.is_in_range(line1_x, inter_y)
        # if other is parallel to the y axis. we know self is for sure not, because they are not parallel
        elif m2 == inf:
            # get the y of the other line at the x value of the inf line
            line2_x = other.p1.x
            inter_y = m1 * line2_x + b1
            return self.is_in_range(line2_x, inter_y) and other.is_in_range(line2_x, inter_y)
        # calculate the x,y of the intersection based on the known formula, but the point may be anywhere in the grid
        inter_x: float = (b2 - b1) / (m1 - m2)
        inter_y: float = m1 * inter_x + b1
        # return True if the point of intersection is exactly on the line cuts that are self and other
        return self.is_in_range(inter_x, inter_y) and other.is_in_range(inter_x, inter_y)

    def walls_intersection_point(self, other: Line) -> Optional[Point]:
        """
        intersecting between walls where one of them is parallel to x axis
        and the second one is parallel to the y axis
        :param other: other line
        :return: intersecting point of the walls. None if no intersection
        """
        if not self.is_intersecting(other):
            return None
        if self.slope() == other.slope():
            return None
        parallel_x = self if self.slope() == 0 else other
        parallel_y = self if other.slope() == 0 else other
        return Point(parallel_y.p1.x, parallel_x.p1.y)

    def __repr__(self):
        return repr(self.p1) + "<->" + repr(self.p2)
