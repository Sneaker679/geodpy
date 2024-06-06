from integration import DiffEquationsSolution
import numpy as np
from sympy import *

# Calculates the velocity as a function of coordinate time (not proper time). This function assumes that DiffEquationsSolution.x0 is time.
def calculate_velocities(velocity_equation : Function, diff_eq_sol: DiffEquationsSolution) -> np.array:
    assert diff_eq_sol.interval is not None and diff_eq_sol.coordinates is not None

    symbolic_args = diff_eq_sol.coordinates.copy()[1:4]
    symbolic_args.extend([coord.diff(diff_eq_sol.interval) for coord in symbolic_args])

    velocity2_equation = velocity_equation ** 2 # Necessary because lambda function doesn't like taking the sqrt of an expression.
    velocity2_equation_lambda = lambdify(symbolic_args, velocity2_equation, "scipy")

    t = diff_eq_sol.x0

    args = []
    args.append(diff_eq_sol.x1)
    args.append(diff_eq_sol.x2)
    args.append(diff_eq_sol.x3)

    for coord in range(3):
        args.append(np.gradient(args[coord],t))

    velocities = velocity2_equation_lambda(*args)**(1/2) # Taking square root to undo the square of earlier.
    velocities[-1] = velocities[-2] # Prevent jagged line at the end.

    return velocities
