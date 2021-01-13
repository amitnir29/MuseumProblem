import time

from Museum import Museum
from MuseumGenerator import generate
from MuseumPrinting import print_museum, print_guards
from optimization import naive_optim, greedy_algo
from pickle_help import *


# TODO generate again the 5 shapes, because we changed name of class
def work_for_map(shape, acc):
    m: Museum = pickle_from_file(f"museums/shape{shape}/acc{acc}")
    print_museum(m)
    start_time = int(round(time.time() * 1000))
    s = greedy_algo(m)
    print(s)
    print_guards(m, s)
    print((int(round(time.time() * 1000)) - start_time) / 1000, "seconds")
    #
    start_time = int(round(time.time() * 1000))
    s = naive_optim(m)
    print(s)
    print_guards(m, s)
    print((int(round(time.time() * 1000)) - start_time) / 1000, "seconds")


if __name__ == '__main__':
    # work_for_map(5, 5)
    for _ in range(4):
        m = generate(20, 5)
        count = 1
        while m is None:
            m = generate(20, 5)
            print(count)
            count += 1
        print(count)
        print_museum(m)

"""
create new map
for acc in range(2,9+1):
        m = Map([--the points], acc)
        s = "museums/dir/acc"+str(acc)
        pickle_to_file(m, s)
        print("finished",acc)
m.print()
"""
