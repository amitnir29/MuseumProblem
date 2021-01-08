# MuseumProblem
The Museum Problem is the following problem:
Given a museum, which is a closed shaped with only right angles, how many guards are needed to protect the whole museum?

In order to solve this problem we wrote code in python which represented the museum and the needed parameters for them.

We used an optimization package called "pulp" in order to solve this problem with Objective, Variables and Constraints we have defined.

## Optimization
* The problem is a binary problen where each "inner" point has a Variable that represents wether there is a guard there or not.
* The Constraints are for each point, the sum of the Variables of all the point who see it will be >= 1 (means it will be seen).
* And lastly, the Objective is the sum of all Variables, whom we wish to minimize.
