from .coordinates import Coordinates

import numpy as np
from sympy import *

### OblongEllipsoid-coordinates class ###
# OblongEllipsoid representation of space-time, used in the Kerr metric example.
class OblongEllipsoid(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('r')(interval), Function('θ')(interval), Function('φ')(interval))
    coords_string: tuple[str]   = ('t', 'r', 'θ', 'φ')
    t, r, θ, φ                  = coords

    @classmethod
    def velocity_equation(cls, **kwargs) -> Function:
        a = kwargs.get('a',0)
        return ( cls.r.diff(cls.interval)**2 * (sin(cls.θ)**2 * cls.r**2/(cls.r**2 + a**2) + cos(cls.θ)**2) + cls.r**2 * cls.θ.diff(cls.interval)**2 + cls.r**2 * cls.φ.diff(cls.interval)**2 * sin(cls.θ)**2 + a**2 * (cls.θ.diff(cls.interval)**2 * cos(cls.θ)**2 + cls.φ.diff(cls.interval)**2 * sin(cls.θ)**2) )**(1/2)

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        a = kwargs.get('a',0)

        r, θ, φ = pos[1:4]

        sinθ = np.sin(θ)

        x = np.sqrt(r*r + a*a) * sinθ * np.cos(φ)
        y = np.sqrt(r*r + a*a) * sinθ * np.sin(φ)
        z = r * np.cos(θ)

        return np.array([pos[0], x, y, z])

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        a = kwargs.get('a',0)

        r, θ = pos[1:3]

        sinθ = np.sin(θ)

        r_sp = np.sqrt(r*r + a*a*sinθ*sinθ)
        θ_sp = np.arctan(np.sqrt(1+a*a/(r*r))*np.tan(θ))

        return np.array([pos[0], r_sp, θ_sp, pos[3]])

