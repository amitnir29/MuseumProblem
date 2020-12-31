from __future__ import annotations

from Point import Point
from math import inf


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1: Point = p1
        self.p2: Point = p2

    def slope(self):
        if self.p1.x == self.p2.x:
            return inf
        return (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)

    def get_mb(self):
        s = self.slope()
        return s, (self.p1.y - s * self.p1.x)

    def is_in_range(self, p: Point):
        return min(self.p1.x, self.p2.x) <= p.x <= max(self.p1.x, self.p2.x) \
               and min(self.p1.y, self.p2.y) <= p.y <= max(self.p1.y, self.p2.y)

    def contains_point(self, p: Point):
        if not self.is_in_range(p):
            return False
        if self.slope() == inf:
            return True
        m, b = self.get_mb()
        return p.y == m * p.x + b

    def is_intersecting(self, other: Line):
        if self.slope() == other.slope():
            return self.contains_point(other.p1) or self.contains_point(other.p2) \
                   or other.contains_point(self.p1) or other.contains_point(self.p2)
        m1, b1 = self.get_mb()
        m2, b2 = other.get_mb()
        inter_x: float = (b2 - b1) / (m1 - m2)
        inter_y: float = m1 * inter_x + b1
        inter_point: Point = Point(inter_x, inter_y)
        return self.is_in_range(inter_point) and other.is_in_range(inter_point)