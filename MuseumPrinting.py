from distributed.deploy.old_ssh import bcolors

from typing import Dict, Tuple, Set

from Museum import Museum
from Point import Point


def print_museum(museum: Museum):
    """
    :param museum: the museum to print
    print the museum grid
    """
    net_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.net)
    wall_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.wall_points)
    min_x, min_y, max_x, max_y = __get_borders(museum)
    # go over the range of possible points in the museum
    for i in range(max_y, min_y - 1, -1):
        for j in range(min_x, max_x + 1):
            p = j, i
            # get position of point relative to the museum, to get the char that represents the role of the point
            if p in net_coordinates:
                if p in wall_coordinates:
                    for p2 in museum.get_wall_points():
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


def print_seen(museum, point_x: int, point_y: int):
    """
    print the museum grid, and mark the input point and all points that see the input point
    :param museum: the museum to print
    :param point_x: x value of the input
    :param point_y: y value of the point
    """
    point = museum.point_from_coordinates(point_x, point_y)
    if point not in museum.net:
        print("not inside map")
        return
    net_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.net)
    wall_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.wall_points)
    seen_by_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.calc_seen_by(point))
    min_x, min_y, max_x, max_y = __get_borders(museum)
    # go over the range of possible points in the museum
    for i in range(max_y, min_y - 1, -1):
        for j in range(min_x, max_x + 1):
            p = j, i
            # get position of point relative to the museum, to get the char that represents the role of the point
            if p[0] == point.x and p[1] == point.y:
                # this is the input point
                print(bcolors.OKGREEN + "X " + bcolors.ENDC, end="")
            else:
                if p in net_coordinates:
                    if p in wall_coordinates:
                        for p2 in museum.get_wall_points():
                            if p2.x == p[0] and p2.y == p[1] and len(p2.walls_on) == 2:
                                if p2.get_coordinates() in seen_by_coordinates:
                                    # mark the point, it sees the input point
                                    print(bcolors.WARNING + "8 " + bcolors.ENDC, end="")
                                else:
                                    print("8 ", end="")
                                break
                        else:
                            if p in seen_by_coordinates:
                                # mark the point, it sees the input point
                                print(bcolors.WARNING + "0 " + bcolors.ENDC, end="")
                            else:
                                print("0 ", end="")
                    else:
                        if p in seen_by_coordinates:
                            # mark the point, it sees the input point
                            print(bcolors.WARNING + "+ " + bcolors.ENDC, end="")
                        else:
                            print("+ ", end="")
                else:
                    print("- ", end="")
        print()


def print_guards(museum, guards: Set[Point]):
    """
    print the museum grid and mark the guard points
    :param museum: the museum to print
    :param guards: the guard points
    """
    net_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.net)
    wall_coordinates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(museum.wall_points)
    guards_cooridnates: Dict[Tuple[int, int], Point] = museum.coordinates_dict(guards)
    min_x, min_y, max_x, max_y = __get_borders(museum)
    # go over the range of possible points in the museum
    for i in range(max_y, min_y - 1, -1):
        for j in range(min_x, max_x + 1):
            p = j, i
            # get position of point relative to the museum, to get the char that represents the role of the point
            if p in net_coordinates:
                if p in wall_coordinates:
                    for p2 in museum.get_wall_points():
                        if p2.x == p[0] and p2.y == p[1] and len(p2.walls_on) == 2:
                            print("8 ", end="")
                            break
                    else:
                        print("0 ", end="")
                else:
                    if p in guards_cooridnates:
                        print(bcolors.OKGREEN + "G " + bcolors.ENDC, end="")
                    else:
                        print("+ ", end="")
            else:
                print("- ", end="")
        print()


def __get_borders(museum: Museum) -> Tuple[int, int, int, int]:
    """
    :param museum: a museum
    :return: (min x,min y, max x, max y)
    """
    min_x = min([p.x for p in museum.corners])
    min_y = min([p.y for p in museum.corners])
    max_x = max([p.x for p in museum.corners])
    max_y = max([p.y for p in museum.corners])
    return min_x, min_y, max_x, max_y
