from .coordinates import Coordinates

import numpy as np
from sympy import *

### Lemaitre-coordinates class ###
# Lemaitre coordinates of space-time cooresponding to a coordinate system where the observer is free-falling towards the origin
# instead of being static, like in a standard sperical coordinate system.
class Lemaitre(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('T')(interval), Function('ρ')(interval), Function('θ')(interval), Function('φ')(interval))
    coords_string: tuple[str]   = ('T', 'ρ', 'θ', 'φ')
    T, ρ, θ, φ                  = coords

    @classmethod
    def velocity_equation(cls, **kwargs) -> Function:
        rs = kwargs.get('rs',1)
        raise NotImplementedError

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        rs = kwargs.get('rs',1)

        T, ρ, θ, φ = pos

        sinθ = np.sin(θ)
        r = (3/2 * (ρ - T))**(2/3) * rs**(1/3)

        cst = 3 * (4*rs*rs/9 * (ρ[0] - T[0]))**(1/3) + rs * (np.log(np.abs( (3/(2*rs) * (ρ[0] - T[0]))**(1/3) - 1 )) - np.log(np.abs( (3/(2*rs) * (ρ[0] - T[0]))**(1/3) + 1 )) )
        t = T - 3 * (4*rs*rs/9 * (ρ - T))**(1/3) - rs * (np.log(np.abs( (3/(2*rs) * (ρ - T))**(1/3) - 1 )) - np.log(np.abs( (3/(2*rs) * (ρ - T))**(1/3) + 1 )) ) + cst
        x = r * sinθ * np.cos(φ)
        y = r * sinθ * np.sin(φ)
        z = r * np.cos(θ)

        return np.array([t, x, y, z])

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        rs = kwargs.get('rs',1)

        T, ρ, θ = pos[0:3]

        sinθ = np.sin(θ)

        cst = 3 * (4*rs*rs/9 * (ρ[0] - T[0]))**(1/3) + rs * (np.log(np.abs( (3/(2*rs) * (ρ[0] - T[0]))**(1/3) - 1 )) - np.log(np.abs( (3/(2*rs) * (ρ[0] - T[0]))**(1/3) + 1 )) )
        t = T - 3 * (4*rs*rs/9 * (ρ - T))**(1/3) - rs * (np.log(np.abs( (3/(2*rs) * (ρ - T))**(1/3) - 1 )) - np.log(np.abs( (3/(2*rs) * (ρ - T))**(1/3) + 1 )) ) + cst
        r = (3/2 * (ρ - T))**(2/3) * rs**(1/3)

        return np.array([t, r, pos[2], pos[3]])


