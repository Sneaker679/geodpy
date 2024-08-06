import numpy as np
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
