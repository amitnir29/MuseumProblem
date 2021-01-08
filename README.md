# MuseumProblem
The Museum Problem is the following problem:
Given a museum, which is a closed shape which has only right angle corners, we want to protect it by placing guards.
A guard can be placed in any point inside the museum, it sees 360 degrees around it (but not through the museum walls), and it cannot move.
We want to place guards in such way that wall points inside the museum (including the walls) can be seen by at least one guard, and thus are safe.
In addition, we want to use the least amount of guards possible.
What is the least amount of guards needed to protect the whole museum, and where should they be placed?

In order to solve this problem we wrote code in python which represents the museum and the needed parameters.

We used an optimization package called "pulp" in order to solve this problem with Objective, Variables and Constraints we have defined.

## Optimization
* The problem is a binary problen where each "inner" point has a Variable that represents wether there is a guard there or not.
* The Constraints are for each point, the sum of the Variables of all the point who see it will be >= 1 (means it will be seen).
* And lastly, the Objective is the sum of all Variables (number of guards), which we wish to minimize.
