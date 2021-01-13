from typing import Set, Dict

from pulp import LpProblem, lpSum, LpVariable, LpMinimize

from Museum import Museum
from Point import Point


def naive_optim(museum: Museum) -> Set[Point]:
    # init the model
    model = LpProblem(name="min_guards_coverage", sense=LpMinimize)
    # create variables:
    # guards variables: is this point a guard (the number of True values should be minimized)
    inner_points: Dict[Point, LpVariable] = {
        p: LpVariable(name=f"inner({p.x},{p.y})", cat="Binary") for p in museum.guards_points}
    # add constrainet
    for point in museum.net:
        point_guards: Set[Point] = museum.calc_seen_by(point)
        point_guards_vars = {p: inner_points[p] for p in point_guards}  # point guards is inside inner points
        model += (lpSum(point_guards_vars.values()) >= 1, f"guarded({point.x},{point.y})")
    # add objective
    model += lpSum(inner_points.values())

    # Solve the optimization problem
    model.solve()

    print(f"objective: {model.objective.value()}")

    return {p for p in inner_points if inner_points[p].value() != 0}


def greedy_algo(museum: Museum) -> Set[Point]:
    seen: Set[Point] = set()
    chosen_guards: Set[Point] = set()
    seen_for_guard: Dict[Point, Set[Point]] = {guard: museum.calc_see(guard) for guard in museum.guards_points}
    while len(seen) != len(museum.net):
        sees_most = max(set(museum.guards_points).difference(chosen_guards),
                        key=lambda guard: len(seen_for_guard[guard].difference(seen)))
        chosen_guards.add(sees_most)
        seen.update(museum.calc_see(sees_most))

    print("number of guards:", len(chosen_guards))
    return chosen_guards

