import time
import matplotlib.pyplot as plt

from Museum import Museum
from MuseumGenerator import generate
from optimization import naive_optim, greedy_algo
from pickle_help import pickle_to_file, pickle_from_file


def create_museums():
    """
    add museums until we stop it
    """
    i = 0
    while True:
        size = random.randint(20, 200)
        acc = random.randint(2, min(5, max(2, 300 // size)))
        print(i, size, acc)
        m = generate(size, acc, False)
        test_object(m, f"test/t{i}")
        i += 1


def test_object(m: Museum, filepath: str):
    """
    solve for input museum. save the solution object:
    (
    museum,
    naive optim guard points unnormialized,
    naive optim guard points normalized as tuples,
    naive optim runtime,
    greedy algo guard points unnormialized,
    greedy algo guard points normalized as tuples,
    greedy algo runtime,
    )
    :param m: a museum
    :param filepath: path of file to save the results object to
    """
    # naive optim:
    start_time = int(round(time.time() * 1000))
    naive_solution = naive_optim(m)
    naive_solution_unnorm = naive_solution
    naive_solution_norm = {(round(p.x / m.acc, 3), round(p.y / m.acc, 3)) for p in naive_solution}
    naive_time = (int(round(time.time() * 1000)) - start_time) / 1000
    # greedy solution:
    start_time = int(round(time.time() * 1000))
    greedy_solution = greedy_algo(m)
    greedy_solution_unnorm = greedy_solution
    greedy_solution_norm = {(round(p.x / m.acc, 3), round(p.y / m.acc, 3)) for p in greedy_solution}
    greedy_time = (int(round(time.time() * 1000)) - start_time) / 1000
    # save to file:
    result_object = (m, naive_solution_unnorm, naive_solution_norm,
                     naive_time, greedy_solution_unnorm, greedy_solution_norm, greedy_time)
    pickle_to_file(result_object, filepath)


def analize_results(number_of_files):
    """
    :param number_of_files: number of files we generated. the files' names are from t0 to t(nof-1)
    """
    results = []
    # get all museums from files
    for i in range(number_of_files):
        o = pickle_from_file(f"test/t{i}")
        results.append(o)
    # separate to naive and greedy
    naive_results = [(i, len(o[1]), o[3]) for i, o in enumerate(results)]
    greedy_results = [(i, len(o[4]), o[6]) for i, o in enumerate(results)]
    print(naive_results)
    print(greedy_results)
    line1, = plt.plot([x[0] for x in naive_results], [x[1] for x in naive_results],c="r")
    line2, = plt.plot([x[0] for x in greedy_results], [x[1] for x in greedy_results],c="g")
    plt.xlabel("museum index")
    plt.ylabel("number of guards")
    plt.legend((line1,line2),("naive","greedy"))
    plt.show()
    line1, = plt.plot([x[0] for x in naive_results], [x[2] for x in naive_results], c="r")
    line2, = plt.plot([x[0] for x in greedy_results], [x[2] for x in greedy_results], c="g")
    plt.xlabel("museum index")
    plt.ylabel("runtime (seconds)")
    plt.legend((line1, line2), ("naive", "greedy"))
    plt.show()
