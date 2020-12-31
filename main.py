import sys

from Line import Line
from Point import Point
from Map import Map
from pickle_help import *

from random import sample

if __name__ == '__main__':
    for acc in range(2,6+1):
        m = Map([Point(0,0),
                Point(5,0),
                Point(5,3),
                Point(3,3),
                Point(3,4),
                Point(6,4),
                Point(6,0),
                Point(7,0),
                Point(7,9),
                Point(3,9),
                Point(3,8),
                Point(5,8),
                Point(5,7),
                Point(3,7),
                Point(3,6),
                Point(5,6),
                Point(5,5),
                Point(2,5),
                Point(2,9),
                Point(1,9),
                Point(1,4),
                Point(0,4),
                Point(0,8),
                Point(-1,8),
                Point(-1,5),
                Point(-2,5),
                Point(-2,7),
                Point(-3,7),
                Point(-3,3),
                Point(1,3),
                Point(1,2),
                Point(4,2),
                Point(4,1),
                Point(0,1)], acc)
        s = "museums/dir/acc"+str(acc)
        pickle_to_file(m, s)
        print("finished",acc)
    m.print()
