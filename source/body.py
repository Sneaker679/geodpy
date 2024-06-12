from typing import Callable

from geodesics import Geodesics

from sympy import *
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.ivp import OdeResult
import numpy as np

class Body:

    def __init__(self, geodesics: Geodesics, position_vec: list, velocity_vec: list) -> None:
        self._geodesics   = geodesics
        self._coordinates = geodesics._coordinates
        self._interval    = geodesics._s
        self.s   = np.array([0])
        self.pos = np.array([[position_vec[0]], [position_vec[1]], [position_vec[2]], [position_vec[3]]])
        self.vel = np.array([[velocity_vec[0]], [velocity_vec[1]], [velocity_vec[2]], [velocity_vec[3]]])
        self.solver_result = None

    def solve_trajectory(
        self,
        time_interval: tuple[float, float],
        method: str = "Radau",
        max_step: float = 1,
        atol: float = 1e-8,
        rtol: float = 1e-8,
        events: Callable = None,
    ) -> bool:

        self.solver_result = solve_ivp(
            fun = Body.__diff_equations_system,
            t_span = time_interval,
            max_step = max_step,
            y0 = np.append(self.pos[:,0], self.vel[:,0]),
            method = method,
            atol = atol,
            rtol = rtol,
            args=(self._geodesics._dₛuᵏ_lambda ,),
            dense_output=False,
            events=events
        )

        self.s   = self.solver_result.t 
        self.pos = self.solver_result.y[0:4]
        self.vel = self.solver_result.y[4:8]

        return self.solver_result.status == 0


    # Solved function
    @staticmethod
    def __diff_equations_system(dτ, state, equations) -> tuple:
        x0, x1, x2, x3, v0, v1, v2, v3  = state

        a0 = equations[0](x0, x1, x2, x3, v0, v1, v2, v3)
        a1 = equations[1](x0, x1, x2, x3, v0, v1, v2, v3)
        a2 = equations[2](x0, x1, x2, x3, v0, v1, v2, v3)
        a3 = equations[3](x0, x1, x2, x3, v0, v1, v2, v3)
        
        return v0, v1, v2, v3, a0, a1, a2, a3
