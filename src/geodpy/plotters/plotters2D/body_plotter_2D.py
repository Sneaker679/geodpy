from ..body_plotter import BodyPlotter

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from abc import ABCMeta, abstractmethod
from copy import deepcopy

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### BodyPlotter2D abstract class ###
# Class that facilitates the plotting of 2D Body objects.
class BodyPlotter2D(BodyPlotter, metaclass=ABCMeta):

    def add_custom_patches(*argv) -> None:
        for patch in argv:
            patch_ani = deepcopy(patch)

            if self.fig is not None:
                patch.set(transform=self.ax.transData._b)
                self.ax.add_patch(patch)

            if self.fig_ani is not None:
                patch_ani.set(transform=self.ax_ani.transData._b)
                self.ax_ani.add_patch(patch_ani)

    def add_circle(self, center: tuple[float, float], radius: float, edgecolor: str, facecolor: str = None, fill: bool = True) -> None:

        circle = patches.Circle(center, radius, edgecolor=edgecolor, fill=fill, facecolor=facecolor)
        circle_ani = deepcopy(circle)

        if self.fig is not None:
            circle.set(transform=self.ax.transData._b)
            self.ax.add_patch(circle)

        if self.fig_ani is not None:
            circle_ani.set(transform=self.ax_ani.transData._b)
            self.ax_ani.add_patch(circle_ani)
