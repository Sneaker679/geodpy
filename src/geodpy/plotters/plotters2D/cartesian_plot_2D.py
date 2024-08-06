from ..body_plotter import BodyPlotter
from .body_plotter_2D import BodyPlotter2D

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from copy import deepcopy

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### CartesianPlot2D class ###
# Class that facilitates the plotting of 2D Body objects expressed in cartesian coordinates.
class CartesianPlot2D(BodyPlotter2D, BodyPlotter):

    def plot(self, title: str) -> None:
        self.fig, self.ax = plt.subplots()
        border = np.max(self.body.pos[1:3]) * 1.2
        self.ax.plot(self.body.pos[1], self.body.pos[2])
        self.ax.set_xlim(-border, border)
        self.ax.set_ylim(-border, border)
        self.ax.set_aspect("equal")
        self.ax.set_title(title)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

    def animate(self, frame_interval: int = 20) -> None:
        self.fig_ani, self.ax_ani = plt.subplots(figsize=(16, 9), dpi=1920/16)
        border = np.max(self.body.pos[1:4]) * 1.2
        line = self.ax_ani.plot(self.body.pos[1], self.body.pos[2])[0]
        self.ax_ani.set_xlim(-border, border)
        self.ax_ani.set_ylim(-border, border)
        self.ax_ani.set_aspect("equal")
        self.ax_ani.set_xlabel("x")
        self.ax_ani.set_ylabel("y")

        def __update_animation(frame, line):
            self.ax_ani.set_title(super(CartesianPlot2D, self)._update_title(frame))
            x = self.body.pos[1][:frame]
            y = self.body.pos[2][:frame]
            line.set_xdata(x)
            line.set_ydata(y)
            return line

        self.ani = animation.FuncAnimation(fig=self.fig_ani, func=__update_animation, save_count=self.body.pos.shape[1], interval=20, fargs=(line, ))

    def info(self, print_info: bool = False) -> None:
        super(CartesianPlot2D, self)._prt_info("2Dcartesian", "t x y z", "x y")
