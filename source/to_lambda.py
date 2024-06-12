from typing import Callable
from sympy import *

# Converts tensor arrays into lambda expressions, for later integration. Array must only depend on coordinates and their first derivative.
def vector_to_lambda(s: Symbol, expressions: Array, coordinates: list[Function]) -> list[Callable]:
    assert expressions.shape[0] == len(coordinates)
    lambda_functions : list[Function] = []
    for k, expr in enumerate(expressions):
        lambda_functions.append(expr_to_lambda(s, expr, coordinates))
    return lambda_functions

def expr_to_lambda(s: Symbol, expression: Function, coordinates: list[Function]) -> Callable:
    args = coordinates.copy()
    args.extend([coord.diff(s) for coord in coordinates])
    return lambdify(args, expression, ["scipy", "numpy"], cse=False, docstring_limit=0)
