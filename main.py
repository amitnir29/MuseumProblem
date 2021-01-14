from Museum import Museum
from MuseumPrinting import print_museum
from Point import Point
from SavedMuseum import create_saved_museum
from SolveMuseum import work_for_museum, work_for_saved_museum
from MuseumGenerator import generate

if __name__ == '__main__':
    m = generate(100, 2, more_unified=False)
    work_for_museum(m)
    # print_museum(m)
