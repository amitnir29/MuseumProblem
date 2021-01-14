import time

from Museum import Museum
from MuseumPrinting import print_museum, print_guards
from optimization import naive_optim, greedy_algo
from pickle_help import pickle_from_file


def work_for_museum(m: Museum):
    """
    solve for input museum
    :param m: a museum
    """
    print_museum(m)
    # naive optim solution:
    print("naive optim:")
    start_time = int(round(time.time() * 1000))
    s = naive_optim(m)
    for p in s:
        print(f"({round(p.x / m.acc, 3)},{round(p.y / m.acc, 3)})", end=" ")
    print()
    print_guards(m, s)
    print((int(round(time.time() * 1000)) - start_time) / 1000, "seconds")
    # greedy solution:
    print("greedy:")
    start_time = int(round(time.time() * 1000))
    s = greedy_algo(m)
    for p in s:
        print(f"({round(p.x / m.acc, 3)},{round(p.y / m.acc, 3)})", end=" ")
    print()
    print_guards(m, s)
    print((int(round(time.time() * 1000)) - start_time) / 1000, "seconds")


def work_for_saved_museum(name: str, acc: int):
    """
    solve for existing museum
    :param name: name of museum
    :param acc: acc value of museum
    """
    m: Museum = pickle_from_file(f"museums/{name}/acc{acc}")
    work_for_museum(m)
