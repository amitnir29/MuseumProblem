from __future__ import annotations

from Point import Point
from math import inf

epsilon = 1e-6


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1: Point = p1
        self.p2: Point = p2

    def slope(self) -> float:
        if self.p1.x == self.p2.x:
            return inf
        return (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)

    def get_mb(self) -> (float, float):
        s = self.slope()
        return s, (self.p1.y - s * self.p1.x)

    def is_in_y_range(self, y: float):
        return min(self.p1.y, self.p2.y) - epsilon <= y <= max(self.p1.y, self.p2.y) + epsilon

    def is_in_x_range(self, x: float):
        return min(self.p1.x, self.p2.x) - epsilon <= x <= max(self.p1.x, self.p2.x) + epsilon

    def is_in_range(self, x: float, y: float):
        return self.is_in_x_range(x) and self.is_in_y_range(y)

    def contains_point(self, p: Point):
        if not self.is_in_range(p.x, p.y):
            return False
        if self.slope() == inf:
            return True
        m, b = self.get_mb()
        return p.y == m * p.x + b

    def is_intersecting(self, other: Line) -> bool:
        if self.slope() == other.slope():
            return self.contains_point(other.p1) or self.contains_point(other.p2) \
                   or other.contains_point(self.p1) or other.contains_point(self.p2)
        m1, b1 = self.get_mb()
        m2, b2 = other.get_mb()
        if m1 == inf:
            # get the y of the other line at the x value of the inf line
            line1_x = self.p1.x
            inter_y = m2 * line1_x + b2
            return self.is_in_range(line1_x, inter_y) and other.is_in_range(line1_x, inter_y)
        elif m2 == inf:
            # get the y of the other line at the x value of the inf line
            line2_x = other.p1.x
            inter_y = m1 * line2_x + b1
            return self.is_in_range(line2_x, inter_y) and other.is_in_range(line2_x, inter_y)
        inter_x: float = (b2 - b1) / (m1 - m2)
        inter_y: float = m1 * inter_x + b1
        return self.is_in_range(inter_x, inter_y) and other.is_in_range(inter_x, inter_y)
