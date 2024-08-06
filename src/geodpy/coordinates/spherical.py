from .coordinates import Coordinates
from .oblong_ellipsoid import OblongEllipsoid

import numpy as np
from sympy import *

### Spherical-OblongEllipsoid-coordinates class ###
# Spherical representation of space-time, used in the Schwarzschild metric example. This is a special case
# of the Oblong Ellipsoid reprensentation when a = 0, "a" being the rotation speed of a blackhole in the Kerr metric.
class Spherical(OblongEllipsoid):

    @classmethod
    def velocity_equation(cls, **kwargs) -> Function:
        return simplify(super(Spherical, Spherical).velocity_equation(a=0))

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        return super(Spherical, Spherical).to_cartesian(pos, a=0)

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        return pos
