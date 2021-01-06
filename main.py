from Map import Map
from pickle_help import *

if __name__ == '__main__':
    m: Map = pickle_from_file("museums/shape5/acc3")
    m.print_seen(6, 10)

"""
create new map
for acc in range(2,9+1):
        m = Map([--the points], acc)
        s = "museums/dir/acc"+str(acc)
        pickle_to_file(m, s)
        print("finished",acc)
m.print()
"""
