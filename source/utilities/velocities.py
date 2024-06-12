from body import Body
import numpy as np
from sympy import *

# Calculates the velocity as a function of coordinate time (not proper time). This function assumes that DiffEquationsSolution.x0 is time.
def calculate_velocities(velocity_equation : Function, body: Body) -> np.array:
    assert body._interval is not None and body._coordinates is not None

    symbolic_args = body._coordinates.copy()[1:4]
    symbolic_args.extend([coord.diff(body._interval) for coord in symbolic_args])

    velocity2_equation = velocity_equation ** 2 # Necessary because lambda function doesn't like taking the sqrt of an expression.
    velocity2_equation_lambda = lambdify(symbolic_args, velocity2_equation, "scipy")

    t = body.pos[0]

    args = []
    args.append(body.pos[1])
    args.append(body.pos[2])
    args.append(body.pos[3])

    for coord in range(3):
        args.append(np.gradient(args[coord],t))

    velocities = velocity2_equation_lambda(*args)**(1/2) # Taking square root to undo the square of earlier.
    velocities[-1] = velocities[-2] # Prevent jagged line at the end.

    return velocities
