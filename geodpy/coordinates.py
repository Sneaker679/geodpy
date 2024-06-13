import numpy as np
from sympy import *

from abc import ABCMeta, abstractmethod

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

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

class Cartesian(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('x')(interval), Function('y')(interval), Function('z')(interval))
    coords_string: tuple[str]   = ('t', 'x', 'y', 'z')
    t, x, y, z                  = coords
    velocity_equation: Function = (coords[1].diff(interval)**2 + coords[2].diff(interval)**2 + coords[3].diff(interval)**2)**(1/2)
    
    def to_cartesian(pos: np.array, **kwargs):
        return pos

class Spherical(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('r')(interval), Function('θ')(interval), Function('φ')(interval))
    coords_string: tuple[str]   = ('t', 'r', 'θ', 'φ')
    t, r, θ, φ                  = coords
    velocity_equation: Function = (r.diff(interval)**2 + r**2 * φ.diff(interval)**2 + r**2 * sin(θ)**2 * θ.diff(interval)**2)**(1/2)

    def to_cartesian(pos: np.array, **kwargs):
        r, θ, φ = pos[1:4]

        sinθ = np.sin(θ)

        x = r * sinθ * np.cos(φ)
        y = r * sinθ * np.sin(φ)
        z = r * np.cos(θ)

        return np.array([pos[0], x, y, z])

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
