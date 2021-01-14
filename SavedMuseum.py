import copy
from typing import List
import os

from Museum import Museum
from MuseumPrinting import print_museum
from Point import Point
from pickle_help import pickle_to_file


def create_saved_museum(name: str, points: List[Point], acc_range: (int, int) = (2, 10), with_prints: bool = True):
    """
    create a directory of an input museum corners
    :param name: name of museum
    :param points: corners of the museum
    :param acc_range: range of acc values to add files of
    :param with_prints: should print during the creation or not
    """
    path = __get_dir(name)
    __create_museum(path, points, acc_range, with_prints)
    __create_build_file(path, points)
    __create_looks_file(path, points)


def __get_dir(name: str) -> str:
    """
    :param name: name of dir
    :return: path of dir
    """
    path = "museums/" + name
    # if does not exist already, create the dir
    if not os.path.isdir(path):
        os.mkdir(path)
    path += "/"
    return path


def __create_museum(path: str, points: List[Point], acc_range: (int, int), with_prints: bool):
    """
    for each acc value, create the museum with this acc and create a file for it
    :param path: path of dir
    :param points: museum corners
    :param acc_range: acc range of museum
    :param with_prints: should print during the process
    """
    for acc in range(acc_range[0], acc_range[1]):
        # create museum
        m = Museum(copy.deepcopy(points), acc)
        s = path + "acc" + str(acc)
        # create file
        pickle_to_file(m, s)
        # print if should
        if with_prints:
            print("finished", acc)
            print_museum(m)


def __create_build_file(path: str, points: List[Point]):
    """
    create file for points to build later if needed
    :param path: path of dir
    :param points: points of the museum
    """
    s = "["
    for point in points[:-1]:
        s += f"Point({point.x},{point.y}),\n"
    s += f"Point({points[-1].x},{points[-1].y})]"
    with open(path + "build.txt", "w") as f:
        f.write(s)


def __create_looks_file(path: str, points: List[Point]):
    """
    create file of the look of the museum
    :param path: path of dir
    :param points: points of museum
    """
    x_values = [p.x for p in points]
    min_x = min(x_values)
    max_x = max(x_values)
    # get acc that creates a print with the best size
    acc = max(2, 50 // (max_x - min_x))
    # create the museum
    museum = Museum(copy.deepcopy(points), acc)
    # print the museum to file
    print_museum(museum, path + "looks.txt")
