from typing import Callable

from geodesics import Geodesics

from sympy import *
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.ivp import OdeResult
import numpy as np

class DiffEquationsSolution:
    def __init__(self, ode_result: OdeResult, geodesics: Geodesics = None):
        self.success: bool = ode_result.status == 0
        self.coordinates = None
        self.interval = None
        self.s: np.array = ode_result.t
        self.x0: np.array = ode_result.y[0]
        self.x1: np.array = ode_result.y[1]
        self.x2: np.array = ode_result.y[2]
        self.x3: np.array = ode_result.y[3]
        self.dx0: np.array = ode_result.y[4]
        self.dx1: np.array = ode_result.y[5]
        self.dx2: np.array = ode_result.y[6]
        self.dx3: np.array = ode_result.y[7]
        self.solver_result = ode_result

        if geodesics is not None:
            self.coordinates = geodesics._coordinates
            self.interval = geodesics._s

# Integrated function
def __diff_equations_system(dτ, state, equations : list) -> tuple:
    assert len(equations) == 4
    x0, x1, x2, x3, v0, v1, v2, v3  = state

    a0 = equations[0](x0, x1, x2, x3, v0, v1, v2, v3)
    a1 = equations[1](x0, x1, x2, x3, v0, v1, v2, v3)
    a2 = equations[2](x0, x1, x2, x3, v0, v1, v2, v3)
    a3 = equations[3](x0, x1, x2, x3, v0, v1, v2, v3)
    
    return v0, v1, v2, v3, a0, a1, a2, a3

# Decorator for solve_ivp
def integrate_diff_eqs(
    geodesics: Geodesics,
    time_interval: tuple[float, float],
    initial_values: list[float],
    method: str = "Radau",
    max_step: float = 1,
    atol: float = 1e-8,
    rtol: float = 1e-8,
    events: Callable = None,
) -> DiffEquationsSolution:

    assert len(initial_values) == 8
    ode_result = solve_ivp(
        fun = __diff_equations_system,
        t_span = time_interval,
        max_step = max_step,
        y0 = initial_values,
        method = method,
        atol = atol,
        rtol = rtol,
        args=(geodesics._dₛuᵏ_lambda ,),
        dense_output=False,
        events=events
    )

    result = DiffEquationsSolution(ode_result, geodesics)

    return result

