from ..geodesics import Geodesics
from ..body import Body
from ..coordinates import Coordinates

from sympy import *
import matplotlib.patches as patches

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### basic function ###
# The examples folder of the project uses this function to execute all its examples.
# This is in order to unify the similar logic/algorithm behind all tests.
def basic(
    coordinates:   Coordinates,
    g_mk:          Matrix,
    initial_pos:   list[float],
    initial_vel:   list[float],
    simplify:      bool,
    solver_kwargs: dict = {},
    verbose:       int  = 0
) -> None:

    # Sets default values in case they were unspecified
    solver_kwargs.setdefault("time_interval", (0,100)                               )
    solver_kwargs.setdefault("method"       , "Radau"                               )
    solver_kwargs.setdefault("max_step"     , solver_kwargs["time_interval"][1]*1e-3)
    solver_kwargs.setdefault("atol"         , 1e-8                                  )
    solver_kwargs.setdefault("rtol"         , 1e-8                                  )
    solver_kwargs.setdefault("events"       , None                                  )

    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(coordinates, g_mk)
    if simplify is True: geodesics.simplify()
    body = Body(geodesics, initial_pos, initial_vel)

    print("Solving trajectory")
    body.solve_trajectory(**solver_kwargs)

    # Printing
    if verbose == 2:
        print("Geodesic differential equations: ")
        for equation in geodesics._dₛuᵏ:
            pprint(equation)
            print()

        print("Integration result: ")
        print(body.solver_result)

    return body
