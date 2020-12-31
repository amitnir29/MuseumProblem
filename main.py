from Line import Line
from Point import Point
from Map import Map

if __name__ == '__main__':
    m = Map([Point(0, 0),
             Point(2, 0),
             Point(2, 1),
             Point(1, 1),
             Point(1, 2),
             Point(2, 2),
             Point(2, 3),
             Point(4, 3),
             Point(4, 4),
             Point(2, 4),
             Point(2, 7),
             Point(-2, 7),
             Point(-2, 6),
             Point(-1, 6),
             Point(-1, 5),
             Point(-2, 5),
             Point(-2, 4),
             Point(0, 4),
             Point(0, 6),
             Point(1, 6),
             Point(1, 3),
             Point(-2, 3),
             Point(-2, 2),
             Point(0, 2)], 4)
    m.print()
    print(m.net)
