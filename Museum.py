from math import inf
from typing import List, Tuple, Set, Dict, Iterable, Union

from Line import Line
from Point import Point


class Museum:
    def __init__(self, corners: List[Point], acc: int):
        if not (type(acc) == int or (type(acc) == float and float(acc).is_integer())):
            raise Exception("acc should be an integer")
        if acc < 2:
            raise Exception("acc should be at least 2")
        self.acc: int = acc  # accuracy level of the map, number of points per 1 length
        self.expand(corners, acc)
        self.corners: List[Point] = corners  # a list of all corners of the museum
        self.walls: List[Line] = self.create_walls(corners)  # a list of all lines of the museum
        self.guards_points: Set[Point] = set()  # a set of all points that can have a guard
        self.wall_points: Set[Point] = set()  # a st of all points that are on a wall
        self.net: Set[Point] = set()  # a set of all points
        self.create_net()  # call the museum creation

    def create_walls(self, corners: List[Point]) -> List[Line]:
        """
        :param corners: a list of points, each to consecutive points represent a wall in the museum
        :return: a list of the walls of the museum, each two consecutive walls are connected by a corner
        """
        walls: List[Line] = []
        for i in range(len(corners)):
            # create a line from the point and the one before it. also works for the last pair of 0 and last(-1)
            walls.append(Line(corners[i - 1], corners[i]))
        # check if all connected walls are parallel to one of the axis
        for wall in walls:
            if wall.slope() != 0 and wall.slope() != inf:
                raise Exception("all walls should be parallel to x axis or y axis")
        # check if all connected walls do not have the same slope
        for i in range(len(walls)):
            if walls[i - 1].slope() == walls[i].slope():
                raise Exception("consecutive walls should have different slope")
        return walls

    def create_net(self) -> None:
        """
        call the functions that create the net points
        """
        self.wall_points: Set[Point] = self.get_wall_points()
        self.guards_points: Set[Point] = self.get_inner_points()
        self.net: Set[Point] = self.wall_points.union(self.guards_points)

    def get_wall_points(self) -> Set[Point]:
        """
        :return: a set of all wall points of the museum
        """
        wall_points: Set[Point] = set()  # init the set
        corners_coordinates: Dict[Tuple[int, int], Point] = dict()  # a dict for corners
        for i, wall in enumerate(self.walls):
            # for each wall, go over all valid points along it and add them to the set
            start, end = wall.p1, wall.p2
            # add the first of the points, which is a corner, and has 2 walls in its walls tuple
            # in case a corner appears twice on the perimeter, we want to have all of its walls
            if start.get_coordinates() not in corners_coordinates:
                # first time seeing for the point. add to wall_points and the dict
                new_start = Point(start.x, start.y, (wall, self.walls[i - 1]))
                wall_points.add(new_start)
                corners_coordinates[start.get_coordinates()] = new_start
            else:
                # first time seeing for the point. update the point's walls
                start_already_defined = corners_coordinates[start.get_coordinates()]
                start_already_defined.walls_on = tuple(list(start_already_defined.walls_on) + [wall, self.walls[i - 1]])
            # now move on to the other points on the wall
            while abs(start.x - end.x) > 1 or abs(start.y - end.y) > 1:
                # move along the wall in the direction needed: up/down/left/right
                start = self.get_next_wall_point(start, end, wall)
                # add the point with the current wall in the walls tuple
                wall_points.add(Point(start.x, start.y, (wall,)))
        return wall_points

    def get_next_wall_point(self, curr: Point, end: Point, wall: Line) -> Point:
        """
        :param wall: wall of the points
        :param curr: current point
        :param end: end point
        :return: the next wall point
        """
        if curr.x == end.x:
            if curr.y < end.y:
                # move the point one step up
                return Point(curr.x, curr.y + 1, (wall,))
            else:
                # move the point one step down
                return Point(curr.x, curr.y - 1, (wall,))
        else:  # y equal
            if curr.x < end.x:
                # move the point one step right
                return Point(curr.x + 1, curr.y, (wall,))
            else:
                # move the point one step left
                return Point(curr.x - 1, curr.y, (wall,))

    def get_inner_neighbors(self, p: Point, wall_points: Dict[Tuple[int, int], Point]) -> Dict[Tuple[int, int], Point]:
        """
        calculates a dict from point coordinates to a point object of all the points
        that are neighbors to the input point by a distance 1
        :param p: an input point
        :param wall_points: a dict from point coordinates to a point object
        :return: the dict
        """
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
        """
        run a bfs on the inner points
        :return: a set of all points the are not ont he walls
        """
        wall_points: Dict[Tuple[int, int], Point] = self.coordinates_dict(self.wall_points)
        inner_points: Set[Point] = set()
        # get a start point for the algorithm
        start_point = self.get_start_point()
        # a set of all points seen already
        seen: Set[Tuple[int, int]] = {start_point.get_coordinates()}
        # the queue of points for the bfs
        curr_points: List[Point] = [start_point]
        while len(curr_points) != 0:
            # get head of queue
            curr_point: Point = curr_points[0]
            # add to result
            inner_points.add(curr_point)
            # remove the head from queue
            curr_points = curr_points[1:]
            # get neighbors of current point
            res = self.get_inner_neighbors(curr_point, wall_points)
            for coords in res:
                # for each neighbor
                if coords in seen:
                    # dont repeated calculation
                    continue
                # add to seen
                seen.add(coords)
                # add the queue
                curr_points.append(res[coords])
        return inner_points

    def get_start_point(self) -> Point:
        """
        get the bottom left corner possible in the range of values.
        if the point is on a wall, it is a corner, and return a point right-above it.
        if it is not on a wall, more to the right until we find a point the is on a wall.
        the found point must be a corner, return the point right-above it.
        :return: the start point for the bfs algorithm (inner point)
        """
        curr_point: Point = self.get_bottom_left_corner()
        while not any([wall.contains_point(curr_point) for wall in self.walls]):
            curr_point.x += 1
        # now we have a bottom corner
        return Point(curr_point.x + 1, curr_point.y + 1)

    def get_bottom_left_corner(self) -> Point:
        """
        :return: the most left bottom point possible for the x,y ranges given of the museum
        """
        return Point(min([p.x for p in self.corners]), min([p.y for p in self.corners]))

    def expand(self, corners: List[Point], acc: int) -> None:
        """
        expand the corners by the expansion factor
        :param corners: a list of corners of the museum
        :param acc: the expansion factor
        """
        for i in range(len(corners)):
            corners[i].x *= acc
            corners[i].y *= acc

    def calc_seen_by(self, point: Point) -> Set[Point]:
        """
        :param point: an input point
        :return: a set of points that see the input point
        """
        seen_by: Set[Point] = set()
        for guard in self.guards_points:
            # for each possible guard point
            guard: Point
            line = Line(guard, point)
            # check if the line between the input point and the guard point intersects with a wall or not
            intersections = [wall for wall in self.walls if line.is_intersecting(wall)]
            intersections = [wall for wall in intersections if wall not in point.walls_on]
            # if not, add to the set
            if len(intersections) == 0:
                seen_by.add(guard)
        return seen_by

    def calc_see(self, guard: Point) -> Set[Point]:
        """
        :param guard: an input inner point
        :return: a set of points that are seen by the input point
        """
        if guard not in self.guards_points:
            return set()
        seen_by: Set[Point] = self.calc_seen_by(guard)
        # add the wall points that are seen by guard
        for wp in self.wall_points:
            line = Line(guard, wp)
            # check if the line between the input point and the guard point intersects with a wall or not
            intersections = [wall for wall in self.walls if line.is_intersecting(wall)]
            intersections = [wall for wall in intersections if wall not in wp.walls_on]
            # if not, add to the set
            if len(intersections) == 0:
                seen_by.add(wp)
        return seen_by

    def point_from_coordinates(self, x, y) -> Union[None, Point]:
        """
        :param x: input x
        :param y: input y
        :return: a point in the museum with these coordinates, None if there is no match
        """
        for p in self.net:
            if p.x == x and p.y == y:
                return p
        return None

    def coordinates_dict(self, points: Iterable[Point]) -> Dict[Tuple[int, int], Point]:
        """
        :param points: an input group if points
        :return: a dict for each point that maps its coordinates to itself
        """
        return {(p.x, p.y): p for p in points}
