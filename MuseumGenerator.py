from __future__ import annotations
from typing import List, Tuple, Dict, FrozenSet
import random

from Museum import Museum
from Point import Point
from Structure import Structure, Square


def generate(min_area: int, acc: int, more_unified: bool = True) -> Museum:
    """
    the main method for the file
    :param min_area: the area of the wanted museum
    :param acc: the acc parameter for the museum
    :param more_unified: should be more unified or more fractured
    :return: the generated museum
    """
    structure: Structure = Structure(more_unified)
    # start square
    start: Square = Square((Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)))
    structure.append(start)
    # add area-1 squares
    for _ in range(min_area - 1):
        add_new_square(structure)
    # convert the squares structure to a points list
    points: List[Point] = get_points_from_structure(structure)
    # create the museum from the points list
    return Museum(points, acc)


def add_new_square(structure: Structure):
    """
    add a new square to the structure
    :param structure: the structure to add a new square to
    :return: True is succeeded
    """
    """
    1. choose a square chosen_square with a free line to add a new square to
    2. create the new square Sn
    3. go over the lines of Sn, if a line exists in another square S',
        update the are_connected dicts of Sn and S' and update the line in both dicts to True
    """
    # part 1
    chosen_square: Square = random.choice(structure.available_squares)
    chosen_line: FrozenSet[Point, Point] = \
        random.choice([k for k, v in chosen_square.are_connected.items() if v is None])
    # part 2
    # check if line is vertical or horizontal:
    line_points: Tuple[Point, ...] = tuple(chosen_line)
    if line_points[0].x == line_points[1].x:
        # this is vertical
        lower_point, upper_point = list(sorted(line_points, key=lambda p: p.y))
        new_point1 = Point(upper_point.x - 1, upper_point.y)
        new_point2 = Point(lower_point.x - 1, lower_point.y)
        if new_point1 in chosen_square.points:
            new_point1.x += 2
            new_point2.x += 2
        new_square = Square((upper_point, new_point1, new_point2, lower_point))
    else:
        # this is horizontal
        left_point, right_point = list(sorted(line_points, key=lambda p: p.x))
        new_point1 = Point(left_point.x, left_point.y - 1)
        new_point2 = Point(right_point.x, right_point.y - 1)
        if new_point1 in chosen_square.points:
            new_point1.y += 2
            new_point2.y += 2
        new_square = Square((left_point, new_point1, new_point2, right_point))
    # part 3
    # go over squares and add relations of squares:
    for line in new_square.are_connected:
        point1, point2 = tuple(line)
        for square in structure.squares:
            if line in square.are_connected:
                new_square.set_connected_value(point1, point2, square)
                square.set_connected_value(point1, point2, new_square)
    # add the square to the structure
    structure.append(new_square)


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
        if s1.get_connected_value(curr_point, p1) is None:
            # option 1. we should go to P1
            curr_point = p1
            continue
        # else, get the other square (S2)
        s2 = s1.get_connected_value(curr_point, p1)
        # get the next potential point (P2)
        neighbors = s2.get_neighbors(curr_point)
        if p1 == neighbors[0]:
            p2 = neighbors[1]
        else:
            p2 = neighbors[0]
        # check if the new line is on two squares:
        if s2.get_connected_value(curr_point, p2) is None:
            curr_point = p2
            curr_square = s2
            continue
        # else, get the 3rd square (P3)
        s3 = s2.get_connected_value(curr_point, p2)
        # now get the other neighbor:
        neighbors = s3.get_neighbors(curr_point)
        if p2 == neighbors[0]:
            p3 = neighbors[1]
        else:
            p3 = neighbors[0]
        # finish, we got P3
        curr_point = p3
        curr_square = s3
    # now we do not want points that are in the middle of lines:
    return remove_middle_points(result_points)


def remove_middle_points(points: List[Point]) -> List[Point]:
    """
    :param points: result points that have points in middle of lines
    :return: the list with only corner points
    """
    result_points: List[Point] = list()
    for i, p in enumerate(points):
        if points[i - 1].x == p.x == points[(i + 1) % len(points)].x:
            continue
        if points[i - 1].y == p.y == points[(i + 1) % len(points)].y:
            continue
        result_points.append(p)
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
