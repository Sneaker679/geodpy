from typing import Callable

from .geodesics import Geodesics
from .coordinates import Cartesian, Spherical

from sympy import *
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.ivp import OdeResult
import numpy as np

### Body class ###
# Class responsible for solving the geodesic differential equation system and storing the results. The class
# can also calculate the norm of the velocity vector and convert itself a cartesian coordinate system.
class Body:

    def __init__(self, geodesics: Geodesics = None, position_vec: list = [0,0,0,0], velocity_vec: list = [0,0,0,0]) -> None:
        self._geodesics   = geodesics
        if geodesics is not None: self._coordinates = geodesics._coordinates
        else: self._coordinates = None

        self.s   = np.array([0])
        self.pos = np.array([[position_vec[0]], [position_vec[1]], [position_vec[2]], [position_vec[3]]])
        self.vel = np.array([[velocity_vec[0]], [velocity_vec[1]], [velocity_vec[2]], [velocity_vec[3]]])
        self.vel_norm = None

        self.solver_result = None

    # Wrapper for scipy.integrate.solve_ivp
    def solve_trajectory(
        self,
        time_interval: tuple[float, float],
        method: str = "Radau",
        max_step: float = 1,
        atol: float = 1e-8,
        rtol: float = 1e-8,
        events: Callable = None,
    ) -> np.array:

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

        return self.s, self.pos, self.vel

    # Function solved with scipy.integrate.solve_ivp
    @staticmethod
    def __diff_equations_system(dτ, state, equations) -> tuple:
        x0, x1, x2, x3, v0, v1, v2, v3  = state

        a0 = equations[0](x0, x1, x2, x3, v0, v1, v2, v3)
        a1 = equations[1](x0, x1, x2, x3, v0, v1, v2, v3)
        a2 = equations[2](x0, x1, x2, x3, v0, v1, v2, v3)
        a3 = equations[3](x0, x1, x2, x3, v0, v1, v2, v3)
        
        return v0, v1, v2, v3, a0, a1, a2, a3

    # Calculates the norm of the velocity vector for each points as a function of coordinate time.
    # This function assumes that self.pos[0] is time.
    def calculate_velocities(self, **kwargs) -> np.array:
        velocity_equation = self._coordinates.velocity_equation(**kwargs)

        # Defining the arguments for the lambda velocity equation
        symbolic_args = list(self._coordinates.coords)[1:4]
        symbolic_args.extend([coord.diff(self._coordinates.interval) for coord in symbolic_args])

        # Making a lambdified velocity equation
        velocity2_equation = velocity_equation ** 2 # Necessary because lambda function doesn't like taking the sqrt of an expression.
        velocity2_equation_lambda = lambdify(symbolic_args, velocity2_equation, ["numpy", "scipy"])

        t = self.pos[0]

        args = []
        args.append(self.pos[1])
        args.append(self.pos[2])
        args.append(self.pos[3])

        # Taking derivative of position vector
        for coord in range(3):
            args.append(np.gradient(args[coord],t))

        self.vel_norm = velocity2_equation_lambda(*args)**(1/2) # Taking square root to undo the square of earlier.
        return self.vel_norm

    # Creates a new Body object from the current body, but represented in cartesian coordinates.
    def get_cartesian_body(self, **kwargs):
        new_body = Body(geodesics = None)
        new_body._coordinates = Cartesian

        new_body.s   = self.s
        new_body.pos = self._coordinates.to_cartesian(self.pos, **kwargs)
        return new_body

    # Creates a new Body object from the current body, but represented in spherical body coordinates.
    def get_spherical_body(self, **kwargs):
        new_body = Body(geodesics = None)
        new_body._coordinates = Spherical

        new_body.s   = self.s
        new_body.pos = self._coordinates.to_spherical(self.pos, **kwargs)
        return new_body
