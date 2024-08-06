from .coordinates import Coordinates

import numpy as np
from sympy import *

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 
### Cartesian-coordinates class ###
# Cartesian representation of space-time
class Cartesian(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('x')(interval), Function('y')(interval), Function('z')(interval))
    coords_string: tuple[str]   = ('t', 'x', 'y', 'z')
    t, x, y, z                  = coords
    
    @classmethod
    def velocity_equation(cls, **kwargs) -> Function:
        return (cls.x.diff(cls.interval)**2 + cls.y.diff(interval)**2 + cls.z.diff(cls.interval)**2)**(1/2)

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        return pos

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        x, y, z = pos[1:4]

        r = np.sqrt(x*x + y*y + z*z) 
        θ = np.arctan(np.sqrt(x*x + y*y)/z)
        φ = np.arctan(y/x)

        return np.array([pos[0], r, θ, φ])
