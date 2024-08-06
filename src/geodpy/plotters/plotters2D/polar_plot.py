from ..body_plotter import BodyPlotter
from .body_plotter_2D import BodyPlotter2D

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

from copy import deepcopy

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### PolarPlot2D class ###
# Class that facilitates the plotting of 2D Body objects expressed in spherical coordinates.
class PolarPlot(BodyPlotter2D, BodyPlotter):

    def plot(self, title: str) -> None:
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "polar"})
        border = np.max(self.body.pos[1]) * 1.2
        self.ax.set_ylim(0, border)
        self.ax.plot(self.body.pos[3], self.body.pos[1])
        self.ax.set_title(title)


    def animate(self, frame_interval: int = 20) -> None:
        self.fig_ani, self.ax_ani = plt.subplots(subplot_kw={"projection": "polar"})
        border = np.max(self.body.pos[1]) * 1.2
        line = self.ax_ani.plot(self.body.pos[3], self.body.pos[1])[0]
        self.ax_ani.set_ylim(0, border)

        def __update_animation(frame, line):
            self.ax_ani.set_title(super(PolarPlot, self)._update_title(frame))
            r = self.body.pos[1][:frame]
            φ = self.body.pos[3][:frame]
            line.set_xdata(φ)
            line.set_ydata(r)
            return line

        self.ani = animation.FuncAnimation(fig=self.fig_ani, func=__update_animation, save_count=self.body.pos.shape[1], interval=20, fargs=(line, ))

    def info(self) -> None:
        super(PolarPlot, self)._prt_info("Polar", "t r θ φ", "r φ", "Note: φ<0,2π>.")
