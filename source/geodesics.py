from typing import Callable
from sympy import *
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.ivp import OdeResult
import numpy as np

class Geodesics:

    def __init__(self, s : Symbol, gₘₖ: Matrix, coordinates: list[Function]):
        assert gₘₖ.shape[0] == len(coordinates)
        assert s not in coordinates
        
        self._s = s
        self._gₘₖ= gₘₖ
        self._coordinates = coordinates
        self._dₛuᵏ= self.__contravariant_acc()
        self._dₛuᵏ_lambda = self.vector_to_lambda(s, self._dₛuᵏ, coordinates)

        self._ode_result : OdeResult = None

    def calculate_velocities(self, velocity_equation : Function) -> np.array:
        assert self._ode_result is not None
        velocity2_equation = velocity_equation ** 2 # Necessary because lambda function doesn't like taking the sqrt of an expression.
        symbolic_args = self._coordinates.copy()[1:4]
        symbolic_args.extend([coord.diff(self._s) for coord in symbolic_args])
        velocity2_equation_lambda = lambdify(symbolic_args, velocity2_equation, "scipy")

        t = self._ode_result.t

        args = list(self._ode_result.y[1:4])
        derivatives = []
        for coord in args:
            derivatives.append(np.gradient(coord,t))

        args.extend(derivatives)
        velocities = velocity2_equation_lambda(*args)**(1/2)
        velocities[-1] = velocities[-2]
        return velocities

    # Geodesic covariant equation : ∂ₛuⱼ = 1/2 * ∂ⱼ(gₘₖ) * uᵐ uᵏ where uᵏ = ∂ₛxᵏ 
    def __covariant_acc(self) -> Array:
        dₛuⱼ: list[Function] = []
        uᵐ  : Array = Array(self._coordinates).diff(self._s)
        uᵐuᵏ: Array = tensorproduct(uᵐ,uᵐ)

        for j, coord in enumerate(self._coordinates):
            dₛuⱼ.append(1/2 * tensorcontraction(tensorproduct(self._gₘₖ.diff(coord), uᵐuᵏ), (0,1,2,3)))
        
        dₛuⱼ= Array(dₛuⱼ)
        return dₛuⱼ

    # Geodesic contravariant equation : ∂ₛuᵏ = gᵐᵏ(∂ₛuₘ - ∂ₛgₘⱼuʲ) where uᵏ = ∂ₛxᵏ
    def __contravariant_acc(self) -> Array:
        dₛuₘ_: Array  = self.__covariant_acc()
        gᵐᵏ_ : Matrix = self._gₘₖ.inv()
        uʲ   : Array  = Array(self._coordinates).diff(self._s)
        
        dₛgₘⱼuʲ= tensorcontraction(tensorproduct( self._gₘₖ.diff(self._s), uʲ              ), (1,2))
        dₛuᵏ   = tensorcontraction(tensorproduct( gᵐᵏ_                   , dₛuₘ_ - dₛgₘⱼuʲ ), (1,2))
        
        return dₛuᵏ

    # Converts tensor arrays into lambda expressions, for later integration. Array must only depend on coordinates and their first derivative.
    @staticmethod
    def vector_to_lambda(s: Symbol, expressions: Array, coordinates: list[Function]) -> list[Callable]:
        assert expressions.shape[0] == len(coordinates)
        lambda_functions : list[Function] = []
        for k, expr in enumerate(expressions):
            lambda_functions.append(Geodesics.expr_to_lambda(s, expr, coordinates))
        return lambda_functions

    @staticmethod
    def expr_to_lambda(s: Symbol, expression: Function, coordinates: list[Function]) -> Callable:
        args = coordinates.copy()
        args.extend([coord.diff(s) for coord in coordinates])
        return lambdify(args, expression, "scipy")

    # Integration methods
    def __diff_equations_system(self, dτ, state, equations : list) -> tuple:
        assert len(equations) == 4
        x0, x1, x2, x3, v0, v1, v2, v3  = state

        a0 = equations[0](x0, x1, x2, x3, v0, v1, v2, v3)
        a1 = equations[1](x0, x1, x2, x3, v0, v1, v2, v3)
        a2 = equations[2](x0, x1, x2, x3, v0, v1, v2, v3)
        a3 = equations[3](x0, x1, x2, x3, v0, v1, v2, v3)
        
        return v0, v1, v2, v3, a0, a1, a2, a3

    def integrate(self, initial_values: list, time_interval : tuple[float,float], max_time_step : float) -> None:
        assert len(initial_values) == 8
        self._ode_result = solve_ivp(
            fun = self.__diff_equations_system,
            t_span = time_interval,
            max_step = max_time_step,
            y0 = initial_values,
            method = "Radau",
            atol = 1e-4,
            rtol = 1e-4,
            args=(self._dₛuᵏ_lambda ,)
        )
        return self._ode_result
