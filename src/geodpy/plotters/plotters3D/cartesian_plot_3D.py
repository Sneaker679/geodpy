from ..body_plotter import BodyPlotter
from .body_plotter_3D import BodyPlotter3D

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### CartesianPlot3D class ###
# Class that facilitates the plotting of Body objects.
class CartesianPlot3D(BodyPlotter3D, BodyPlotter):

    def plot(self, title: str) -> None:
        self.fig, self.ax = plt.subplots(subplot_kw={"projection":"3d", "computed_zorder": False})
        border = np.max(self.body.pos[1:3]) * 1.2
        self.ax.plot(self.body.pos[1], self.body.pos[2], self.body.pos[3])
        self.ax.set_xlim(-border, border)
        self.ax.set_ylim(-border, border)
        self.ax.set_zlim(-border, border)
        self.ax.set_aspect("equal")
        self.ax.set_title(title)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")


    # Animation plotting methods
    def animate(self, frame_interval: int = 20) -> None:
        self.fig_ani, self.ax_ani = plt.subplots(subplot_kw={"projection":"3d", "computed_zorder": False})
        border = np.max(self.body.pos[1:4]) * 1.2
        line = self.ax_ani.plot(self.body.pos[1], self.body.pos[2], self.body.pos[3])[0]
        self.ax_ani.set_xlim(-border, border)
        self.ax_ani.set_ylim(-border, border)
        self.ax_ani.set_zlim(-border, border)
        self.ax_ani.set_aspect("equal")
        self.ax_ani.set_xlabel("x")
        self.ax_ani.set_ylabel("y")
        self.ax_ani.set_zlabel("z")

        def __update_animation(frame, line):
            self.ax_ani.set_title(super(CartesianPlot3D, self)._update_title(frame))
            x = self.body.pos[1][:frame]
            y = self.body.pos[2][:frame]
            z = self.body.pos[3][:frame]
            line.set_data_3d(x, y, z)
            return line

        self.ani = animation.FuncAnimation(fig=self.fig_ani, func=__update_animation, save_count=self.body.pos.shape[1], interval=20, fargs=(line, ))

    def info(self) -> None:
        super(CartesianPlot3D, self)._prt_info("3Dcartesian", "t x y z", "x y z")

