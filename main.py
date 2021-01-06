from Map import Map
from Point import Point
from pickle_help import *
from optimization import optim

if __name__ == '__main__':
    m: Map = pickle_from_file("museums/shape4/acc3")
    m.print()
    s = optim(m)
    print(s)
    m.print_guards(s)

"""
create new map
for acc in range(2,9+1):
        m = Map([--the points], acc)
        s = "museums/dir/acc"+str(acc)
        pickle_to_file(m, s)
        print("finished",acc)
m.print()
"""
