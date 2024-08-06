from ..body_plotter import BodyPlotter

from sympy import *
import matplotlib.pyplot as plt
import numpy as np

from abc import ABCMeta, abstractmethod

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 


### BodyPlotter3D abstract class ###
# Class that facilitates the plotting of 3D Body objects.
class BodyPlotter3D(BodyPlotter, metaclass=ABCMeta):

    def add_custom_surface(self, x: np.array, y: np.array, z: np.array, facecolor: str = 'k') -> None:
        if self.fig is not None: self.ax.plot_surface(x, y, z, color=facecolor, zorder=1, shade=False)
        if self.fig_ani is not None: self.ax_ani.plot_surface(x, y, z, color=facecolor, zorder=1, shade=False)

    def add_sphere(self, center: tuple[float, float], radius: float, facecolor: str) -> None:
        θ, φ = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
        x = radius * np.sin(θ) * np.cos(φ) + center[0]
        y = radius * np.sin(θ) * np.sin(φ) + center[1]
        z = radius * np.cos(θ) + center[2]
        self.add_custom_surface(x, y, z, facecolor=facecolor)
