import numpy as np
from sympy import *

from abc import ABCMeta, abstractmethod

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

### Coordinates class ###
# This abstract class is the base template for all coordinate systems implemented as classes.
class Coordinates(metaclass=ABCMeta):
    @property
    @abstractmethod
    def interval():
        pass

    @property
    @abstractmethod
    def coords():
        pass

    @property
    @abstractmethod
    def velocity_equation():
        pass

    @property
    @abstractmethod
    def coords_string():
        pass

    @abstractmethod
    def to_cartesian(pos: np.array, **kwargs):
        pass

#### Coordinate systems ####

### Cartesian-coordinates class ###
# Cartesian representation of space-time
class Cartesian(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('x')(interval), Function('y')(interval), Function('z')(interval))
    coords_string: tuple[str]   = ('t', 'x', 'y', 'z')
    t, x, y, z                  = coords
    velocity_equation: Function = (coords[1].diff(interval)**2 + coords[2].diff(interval)**2 + coords[3].diff(interval)**2)**(1/2)
    
    def to_cartesian(pos: np.array, **kwargs):
        return pos

### OblongEllipsoid-coordinates class ###
# OblongEllipsoid representation of space-time, used in the Kerr metric example.
class OblongEllipsoid:
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('r')(interval), Function('θ')(interval), Function('φ')(interval))
    coords_string: tuple[str]   = ('t', 'r', 'θ', 'φ')
    t, r, θ, φ                  = coords
    velocity_equation: Function = (r.diff(interval)**2 + r**2 * φ.diff(interval)**2 + r**2 * sin(θ)**2 * θ.diff(interval)**2)**(1/2)

    def to_cartesian(pos: np.array, **kwargs):
        a = kwargs.get('a',0)

        r, θ, φ = pos[1:4]

        sinθ = np.sin(θ)

        x = np.sqrt(r*r + a*a) * sinθ * np.cos(φ)
        y = np.sqrt(r*r + a*a) * sinθ * np.sin(φ)
        z = r * np.cos(θ)

        return np.array([pos[0], x, y, z])

### Spherical-oblongellipsoid-coordinates class ###
# Spherical representation of space-time, used in the Schwarzschild metric example. This is a special case
# of the Oblong Ellipsoid reprensentation when a = 0, "a" being the rotation speed of a blackhole in the Kerr metric.
class Spherical(OblongEllipsoid):
    def to_cartesian(pos: np.array, **kwargs):
        return super().to_cartesian(pos, a=0)

