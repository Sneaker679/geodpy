import numpy as np
from sympy import *

from abc import ABCMeta, abstractmethod

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

### Coordinates abstract class ###
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
    def coords_string():
        pass

    @abstractmethod
    def velocity_equation(cls, **kwargs):
        pass

    @abstractmethod
    def to_cartesian(pos: np.array, **kwargs):
        pass

    @abstractmethod
    def to_spherical(pos: np.array, **kwargs):
        pass


#### Coordinate systems ####

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

### Spherical-oblongellipsoid-coordinates class ###
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
