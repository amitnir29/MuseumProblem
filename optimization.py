from typing import Set, Dict

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpMinimize, LpSolver

from Map import Map
from Point import Point


def optim(museum: Map) -> Set[Point]:
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
