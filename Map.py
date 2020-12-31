from typing import List, Tuple, Set

from Line import Line
from Point import Point


class Map:
    def __init__(self, corners: List[Point], acc: int):
        self.acc: int = acc
        self.step_size: float = 1 / acc
        self.corners: List[Point] = corners
        self.walls: List[Line] = self.create_walls(corners)
        self.net: List[Point] = self.create_net()

    def create_walls(self, corners: List[Point]) -> List[Line]:
        walls: List[Line] = []
        for i in range(len(corners) - 1):
            walls.append(Line(corners[i], corners[i + 1]))
            corners[i].walls_on.append(walls[-1])
            corners[i + 1].walls_on.append(walls[-1])
        walls.append(Line(corners[-1], corners[0]))
        corners[0].walls_on.append(walls[-1])
        corners[-1].walls_on.append(walls[-1])
        return walls

    def create_net(self) -> List[Point]:
        wall_points = self.get_wall_points()
        return wall_points + self.get_inner_points({(p.x, p.y) for p in wall_points})

    def get_wall_points(self) -> List[Point]:
        wall_points: List[Point] = []
        for wall in self.walls:
            start, end = wall.p1, wall.p2
            while start.x != end.x or start.y != end.y:
                wall_points.append(start)
                if start.x == end.x:
                    if start.y < end.y:
                        start = Point(start.x, start.y + self.step_size, [wall])
                    else:
                        start = Point(start.x, start.y - self.step_size, [wall])
                else:  # y equal
                    if start.x < end.x:
                        start = Point(start.x + self.step_size, start.y, [wall])
                    else:
                        start = Point(start.x - self.step_size, start.y, [wall])
        return wall_points

    def get_inner_neighbors(self, p: Point, wall_points: Set[Tuple[float, float]]) -> \
            (List[Point], List[Tuple[float, float]]):
        neighbors: List[Point] = []
        neighbors_coordinates: List[Tuple[float, float]] = []
        up = (p.x, p.y + self.step_size)
        if up not in wall_points:
            neighbors.append(Point(up[0], up[1]))
            neighbors_coordinates.append(up)
        down = (p.x, p.y - self.step_size)
        if down not in wall_points:
            neighbors.append(Point(down[0], down[1]))
            neighbors_coordinates.append(down)
        right = (p.x + self.step_size, p.y)
        if right not in wall_points:
            neighbors.append(Point(right[0], right[1]))
            neighbors_coordinates.append(right)
        left = (p.x - self.step_size, p.y)
        if left not in wall_points:
            neighbors.append(Point(left[0], left[1]))
            neighbors_coordinates.append(left)
        return neighbors, neighbors_coordinates

    def get_inner_points(self, wall_points: Set[Tuple[float, float]]) -> List[Point]:
        inner_points: List[Point] = []
        start_point = self.get_start_point()
        seen: Set[Tuple[float, float]] = {start_point.get_coordinates()}
        curr_points: List[Point] = [start_point]
        while len(curr_points) != 0:
            curr_point: Point = curr_points[0]
            inner_points.append(curr_point)
            curr_points = curr_points[1:]
            res = self.get_inner_neighbors(curr_point, wall_points)
            for p, coords in zip(res[0], res[1]):
                if coords in seen:
                    continue
                seen.add(coords)
                curr_points.append(p)
        return inner_points

    def get_start_point(self) -> Point:
        curr_point: Point = self.get_bottom_left_corner()
        while not any([wall.contains_point(curr_point) for wall in self.walls]):
            curr_point.x += self.step_size
        # now we have a bottom corner
        return Point(curr_point.x + self.step_size, curr_point.y + self.step_size)

    def get_bottom_left_corner(self) -> Point:
        return Point(min([p.x for p in self.corners]), min([p.y for p in self.corners]))

    def print(self):
        net_coordinates: Set[(float, float)] = {p.get_coordinates() for p in self.net}
        wall_coordinates:Set[(float,float)] = {p.get_coordinates() for p in self.get_wall_points()}
        min_x = min([p.x for p in self.corners])
        min_y = min([p.y for p in self.corners])
        max_x = max([p.x for p in self.corners])
        max_y = max([p.y for p in self.corners])
        for i in range(int(max_y * self.acc), int(min_y * self.acc) - 1, -1):
            for j in range(int(min_x * self.acc), int(max_x * self.acc) + 1):
                p = j / self.acc, i / self.acc
                if p in net_coordinates:
                    if p in wall_coordinates:
                        print("0",end="")
                    else:
                        print("+", end="")
                else:
                    print("-", end="")
            print()
