from typing import List, Tuple, Set, Dict, Iterable
from itertools import combinations

from distributed.deploy.old_ssh import bcolors

from Line import Line
from Point import Point


class Map:
    def __init__(self, corners: List[Point], acc: int):
        self.acc: int = acc
        self.expand(corners, acc)
        self.corners: List[Point] = corners
        self.walls: List[Line] = self.create_walls(corners)
        self.guards_points: Set[Point] = set()
        self.wall_points: Set[Point] = set()
        self.net: Set[Point] = set()
        self.create_net()

    def create_walls(self, corners: List[Point]) -> List[Line]:
        walls: List[Line] = []
        for i in range(len(corners)):
            walls.append(Line(corners[i - 1], corners[i]))
        return walls

    def create_net(self) -> None:
        self.wall_points: Set[Point] = self.get_wall_points()
        self.guards_points: Set[Point] = self.get_inner_points()
        self.net: Set[Point] = self.wall_points.union(self.guards_points)

    def get_wall_points(self) -> Set[Point]:
        wall_points: Set[Point] = set()
        for i, wall in enumerate(self.walls):
            start, end = wall.p1, wall.p2
            wall_points.add(Point(start.x, start.y, (wall, self.walls[i - 1])))
            while abs(start.x - end.x) > 1 or abs(start.y - end.y) > 1:
                if start.x == end.x:
                    if start.y < end.y:
                        start = Point(start.x, start.y + 1, (wall,))
                    else:
                        start = Point(start.x, start.y - 1, (wall,))
                else:  # y equal
                    if start.x < end.x:
                        start = Point(start.x + 1, start.y, (wall,))
                    else:
                        start = Point(start.x - 1, start.y, (wall,))
                wall_points.add(Point(start.x, start.y, (wall,)))
        return wall_points

    def get_inner_neighbors(self, p: Point, wall_points: Dict[Tuple[int, int], Point]) -> Dict[Tuple[int, int], Point]:
        neighbors: Dict[Tuple[int, int], Point] = dict()
        up = (p.x, p.y + 1)
        if up not in wall_points:
            neighbors[up] = Point(up[0], up[1])
        down = (p.x, p.y - 1)
        if down not in wall_points:
            neighbors[down] = Point(down[0], down[1])
        right = (p.x + 1, p.y)
        if right not in wall_points:
            neighbors[right] = Point(right[0], right[1])
        left = (p.x - 1, p.y)
        if left not in wall_points:
            neighbors[left] = Point(left[0], left[1])
        return neighbors

    def get_inner_points(self) -> Set[Point]:
        wall_points: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.wall_points)
        inner_points: Set[Point] = set()
        start_point = self.get_start_point()
        seen: Set[Tuple[int, int]] = {start_point.get_coordinates()}
        curr_points: List[Point] = [start_point]
        while len(curr_points) != 0:
            curr_point: Point = curr_points[0]
            inner_points.add(curr_point)
            curr_points = curr_points[1:]
            res = self.get_inner_neighbors(curr_point, wall_points)
            for coords in res:
                if coords in seen:
                    continue
                seen.add(coords)
                curr_points.append(res[coords])
        return inner_points

    def get_start_point(self) -> Point:
        curr_point: Point = self.get_bottom_left_corner()
        while not any([wall.contains_point(curr_point) for wall in self.walls]):
            curr_point.x += 1
        # now we have a bottom corner
        return Point(curr_point.x + 1, curr_point.y + 1)

    def get_bottom_left_corner(self) -> Point:
        return Point(min([p.x for p in self.corners]), min([p.y for p in self.corners]))

    def print(self):
        net_coordinates: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.net)
        wall_coordinates: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.wall_points)
        min_x = min([p.x for p in self.corners])
        min_y = min([p.y for p in self.corners])
        max_x = max([p.x for p in self.corners])
        max_y = max([p.y for p in self.corners])
        for i in range(max_y, min_y - 1, -1):
            for j in range(min_x, max_x + 1):
                p = j, i
                if p in net_coordinates:
                    if p in wall_coordinates:
                        for p2 in self.get_wall_points():
                            if p2.x == p[0] and p2.y == p[1] and len(p2.walls_on) == 2:
                                print("8 ", end="")
                                break
                        else:
                            print("0 ", end="")
                    else:
                        print("+ ", end="")
                else:
                    print("- ", end="")
            print()

    def print_seen(self, point_x: int, point_y: int):
        point = self.point_from_coordinates(point_x, point_y)
        net_coordinates: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.net)
        wall_coordinates: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.wall_points)
        seen_by_coordinates: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.calc_seen_by(point))
        min_x = min([p.x for p in self.corners])
        min_y = min([p.y for p in self.corners])
        max_x = max([p.x for p in self.corners])
        max_y = max([p.y for p in self.corners])
        for i in range(max_y, min_y - 1, -1):
            for j in range(min_x, max_x + 1):
                p = j, i
                if p[0] == point.x and p[1] == point.y:
                    print(bcolors.OKGREEN + "X " + bcolors.ENDC, end="")
                else:
                    if p in net_coordinates:
                        if p in wall_coordinates:
                            for p2 in self.get_wall_points():
                                if p2.x == p[0] and p2.y == p[1] and len(p2.walls_on) == 2:
                                    if p2.get_coordinates() in seen_by_coordinates:
                                        print(bcolors.WARNING + "8 " + bcolors.ENDC, end="")
                                    else:
                                        print("8 ", end="")
                                    break
                            else:
                                if p in seen_by_coordinates:
                                    print(bcolors.WARNING + "0 " + bcolors.ENDC, end="")
                                else:
                                    print("0 ", end="")
                        else:
                            if p in seen_by_coordinates:
                                print(bcolors.WARNING + "+ " + bcolors.ENDC, end="")
                            else:
                                print("+ ", end="")
                    else:
                        print("- ", end="")
            print()

    def expand(self, corners: List[Point], acc: int) -> None:
        for i in range(len(corners)):
            corners[i].x *= acc
            corners[i].y *= acc

    def calc_seen_by(self, point: Point) -> Set[Point]:
        seen_by: Set[Point] = set()
        for guard in self.guards_points:
            guard: Point
            line = Line(guard, point)
            intersections = [wall for wall in self.walls if line.is_intersecting(wall)]
            intersections = [wall for wall in intersections if wall not in point.walls_on]
            if len(intersections) == 0:
                seen_by.add(guard)
        return seen_by

    def point_from_coordinates(self, x, y) -> Point:
        for p in self.net:
            if p.x == x and p.y == y:
                return p
        return None

    def coordinates_dict(self, points: Iterable[Point]) -> Dict[Tuple[int, int], Point]:
        return {(p.x, p.y): p for p in points}
