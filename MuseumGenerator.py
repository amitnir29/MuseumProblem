from collections import defaultdict
from typing import List, Optional, Tuple, Dict, FrozenSet

from Museum import Museum
from Point import Point


# def generate(max_walls: int, acc: int=2) -> Optional[Museum]:
#     walls: List[Line] = []
#     start = Point(0, 0)
#
#     direction = get_rand_direction()
#     curr: Point = start.add_coordinates(direction * get_rand_length())
#     last_point = curr
#     walls.append(Line(start, curr))
#     for _ in range(max_walls):
#         direction = get_rand_direction(direction)
#         curr = curr.add_coordinates(direction * get_rand_length())
#         new_wall = Line(last_point, curr)
#         last_point = curr
#         if intersects(walls[:-1], new_wall) is not None:
#             walls.append(new_wall)
#             break
#         walls.append(new_wall)
#     else:
#         return None
#     # get the museum
#     intersecting_wall_index = intersects(walls[:-2], walls[-1])
#     intersecting_walls: Tuple[Line, Line] = (walls[-1], walls[intersecting_wall_index])
#     inter_point = intersecting_walls[0].walls_intersection_point(intersecting_walls[1])
#     walls = [Line(inter_point, walls[intersecting_wall_index].p2)] + \
#             walls[intersecting_wall_index + 1:-1] + [Line(walls[-1].p1, inter_point)]
#     # get points
#     corners: List[Point] = list()
#     for wall in walls:
#         corners.append(wall.p1)
#     return Museum(corners, acc)
#
#
# def get_rand_direction(prev: Tuple[int, int] = None) -> Tuple[int, int]:
#     RIGHT: Tuple[int, int] = (1, 0)
#     LEFT: Tuple[int, int] = (-1, 0)
#     UP: Tuple[int, int] = (0, 1)
#     DOWN: Tuple[int, int] = (0, -1)
#     directions: List[Tuple[int, int]] = [RIGHT, LEFT, UP, DOWN]
#     if prev is None:
#         return random.choice(directions)
#     if prev in directions[:2]:
#         return random.choice(directions[2:])
#     if prev in directions[2:]:
#         return random.choice(directions[:2])
#     return None
#
#
# def get_rand_length() -> int:
#     return random.randint(1, 10)
#
#
# def intersects(walls: List[Line], new_wall: Line) -> Optional[int]:
#     for i, wall in enumerate(walls):
#         if new_wall.walls_intersection_point(wall) is not None:
#             return i
#     return None

class Square:
    def __init__(self, points: Tuple[Point, Point, Point, Point]):
        self.points: Tuple[Point, Point, Point, Point] = points
        self.__are_connected: Dict[FrozenSet[Point, Point], bool] = self.create_connected_dict()

    def get_neighbors(self, point: Point) -> Optional[Tuple[Point, Point]]:
        """
        :param point: input point
        :return: the neighbor points of the input point in the square
        """
        if point not in self.points:
            return None
        index = self.points.index(point)
        # return the prev and next points
        return self.points[index - 1], self.points[index + 1]

    def get_connected_value(self, p1, p2) -> Optional[bool]:
        """
        getter for a points pair in the dict
        :param p1: one point
        :param p2: second point
        :return: the value of the pair in the dict, None if not in the dict
        """
        pair = frozenset((p1, p2))
        if pair not in self.__are_connected:
            return None
        return self.__are_connected[pair]

    def set_connected_value(self, p1, p2, value):
        """
        setter for a points pair in the dict
        :param p1: one point
        :param p2: second point
        :param value: new value for the pair in the dict
        """
        self.__are_connected[frozenset((p1, p2))] = value

    def create_connected_dict(self) -> Dict[FrozenSet[Point, Point], bool]:
        """
        :return: a dict from each neighbor points to False
        """
        res: Dict[FrozenSet[Point, Point], bool] = dict()
        for i in range(len(self.points)):
            self.set_connected_value(self.points[i], self.points[i - 1], False)
        return res


class Structure:
    def __init__(self, allow_big_areas=True):
        self.squares: List[Square] = list()
        self.allow_big_areas: bool = allow_big_areas  # TODO

    def append(self, square: Square):
        """
        add the square to the list of squares
        :param square: a new square
        """
        self.squares.append(square)

    def get_all_points(self) -> Dict[Point, List[Square]]:
        """
        :return: a dict from each point to the squares it is on
        """
        results: Dict[Point, List[Square]] = defaultdict(list)
        for square in self.squares:
            for p in square.points:
                results[p].append(square)
        return results

    def squares_on(self, p1, p2) -> List[Square]:
        """
        :param p1: one point
        :param p2: second point
        :return: a list of squares that the line (p1,p2) is on them
        """
        result: List[Square] = list()
        for square in self.squares:
            if square.get_connected_value(p1, p2) is not None:
                result.append(square)
        return result


def generate(area, acc, allow_big_areas=True) -> Museum:
    """
    the main method for the file
    :param area: the area of the wanted museum
    :param acc: the acc parameter for the museum
    :param allow_big_areas: boolean for the shape of the museum
    :return: the generated museum
    """
    structure: Structure = Structure(allow_big_areas)
    # start square
    start: Square = Square((Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)))
    structure.append(start)
    # add area-1 squares
    for _ in range(area - 1):
        add_new_square(structure)
    # convert the squares structure to a points list
    points: List[Point] = get_points_from_structure(structure)
    # create the museum from the points list
    return Museum(points, acc)


def add_new_square(structure: Structure) -> None:  # TODO
    """
    add a new square to the structure
    :param structure: the structure to add a new square to
    """
    return None


def get_points_from_structure(structure: Structure) -> List[Point]:
    """
    get a starting point and move along the perimeter until we get back to the point.
    :param structure: a structure of squares
    :return: a list of points that represent the arc of the museum
    """
    # a dict of points to squares
    all_points = structure.get_all_points()
    # start point of
    start_point = get_start_point(structure, all_points)
    # current square. index 0 because start_point is for sure only on one square
    curr_square: Square = all_points[start_point][0]
    # a random neighbor of the start point
    curr_point = curr_square.get_neighbors(start_point)[0]
    # create the result list, starting with start_point
    result_points: List[Point] = [start_point]
    # while we have not reached the start point back
    while curr_point != start_point:
        # add the point to the list
        result_points.append(curr_point)
        """
        now we have one of 3 options:
        we should look at the other neighbor of the current point (the neighbor we did not come from), mark P1
        now look at the line (curr,P1), and we are on the square S1.
        1. if the line is on exactly one square (S1), then we must continue to P1, no other options.
        else, we can not move to P1, that would be moving through the structure.
        we see that P1 is also a neighbor of the current point on the other square (mark as S2).
        lets look at the other neighbor of the current point in S2, mark as P2.
        2. if the line (curr,p2) is on exactly one square, we should move to P2.
        else, we can not move to P2, that would be moving through the structure.
        so, we see that P2 is also a neighbor of the current point on the other square (mark as S3).
        lets look at the other neighbor of the current point in S3, mark as P3.
        3. this point must be the point to go to, return P3.
        """
        prev_point = result_points[-2]
        s1: Square = curr_square
        # get the other neighbor of curr in S1 (P1)
        if s1.get_neighbors(curr_point)[0] == prev_point:
            p1 = curr_square.get_neighbors(curr_point)[1]
        else:
            p1 = curr_square.get_neighbors(curr_point)[0]
        # now check if this line is also on another square
        squares_on = structure.squares_on(curr_point, p1)
        if len(squares_on) == 1:
            # option 1. we should go to P1
            curr_point = p1
            continue
        # else, get the other square (S2)
        if squares_on[0] == s1:
            s2 = squares_on[1]
        else:
            s2 = squares_on[0]
        # get the next potential point (P2)
        neighbors = s2.get_neighbors(curr_point)
        if p1 == neighbors[0]:
            p2 = neighbors[1]
        else:
            p2 = neighbors[0]
        # check if the new line is on two squares:
        squares_on = structure.squares_on(curr_point, p2)
        if len(squares_on) == 1:
            curr_point = p2
            curr_square = s2
            continue
        # else, get the 3rd square (P3)
        if squares_on[0] == s2:
            s3 = squares_on[1]
        else:
            s3 = squares_on[0]
        # now get the other neighbor:
        neighbors = s3.get_neighbors(curr_point)
        if p2 == neighbors[0]:
            p3 = neighbors[1]
        else:
            p3 = neighbors[0]
        # finish, we got P3
        curr_point = p3
        curr_square = s3
    return result_points


def get_start_point(structure: Structure, all_points: Dict[Point, List[Square]]) -> Point:
    """
    :param structure: the structure of the squares
    :param all_points: dict from points to squares on
    :return: the starting point
    """
    # start at the bottom left corner
    point = Point(min([p.x for square in structure.squares for p in square.points]),
                  min([p.y for square in structure.squares for p in square.points]))
    # go to the right until we arrive to a point that is on the structure
    while point not in all_points:
        point.x += 1
    return point
