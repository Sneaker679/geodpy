from .coordinates import Coordinates

from typing import Callable

from sympy import *

# Converts tensor arrays into lambda expressions, for later integration. Array must only depend on coordinates and their first derivative.
def vector_to_lambda(coordinates: Coordinates, expressions: Array) -> list[Callable]:
    assert expressions.shape[0] == len(coordinates.coords)
    lambda_functions : list[Function] = []
    for k, expr in enumerate(expressions):
        lambda_functions.append(expr_to_lambda(coordinates, expr))
    return lambda_functions

def expr_to_lambda(coordinates: Coordinates, expression: Function) -> Callable:
    args = list(coordinates.coords)
    args.extend([coord.diff(coordinates.interval) for coord in coordinates.coords])
    return lambdify(args, expression, ["scipy", "numpy"], cse=False, docstring_limit=0)
