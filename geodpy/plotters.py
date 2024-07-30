from .body import Body

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

from abc import ABCMeta, abstractmethod
from copy import deepcopy

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### BodyPlotter abstract class ###
# Class that facilitates the plotting of Body objects.
class BodyPlotter(metaclass=ABCMeta):
    
    def __init__(self, body: Body) -> None:
        self.body = body
        self.coordinates = body._coordinates

        self.fig, self.ax = None, None
        self.fig_ani, self.ax_ani = None, None
        self.fig_vel, self.ax_vel = None, None

        self.ani = None


    # Orbit plotting methods
    @abstractmethod
    def plot(self, title: str) -> None:
        pass

    def save_plot(self, file_name: str = "body") -> None:
        if file_name[-4:] != ".pdf" and file_name[-4:] != ".png":
            file_name += ".pdf"
        self.fig.savefig(file_name)


    # Animation plotting methods
    @abstractmethod
    def animate(self, frame_interval: int = 20) -> None:
        pass

    def _update_title(self,frame: int) -> str:
        lenght = len(self.body.pos[0])
        if frame >= lenght:
            frame = lenght - 1

        s = '{:e}'.format(self.body.s[frame]),
        pos = [
            '{:e}'.format(self.body.pos[0][frame]),
            '{:e}'.format(self.body.pos[1][frame]),
            '{:e}'.format(self.body.pos[2][frame]),
            '{:e}'.format(self.body.pos[3][frame])
        ]

        title = f"s= {s},"
        for i, coord in enumerate(self.coordinates.coords_string):
            title = ''.join([title, f" {coord}= {pos[i]}"])
            if i != 3:
                title = ''.join([title, ","])

        return title

    def save_animation(self, file_name: str = "body", dpi=100) -> None:
        if file_name[-4:] != ".mp4":
            file_name += ".mp4"
        self.ani.save(file_name, dpi=dpi)


    # Velocity plot methods
    def plot_velocity(self, title: str) -> None:
        assert self.body.vel_norm is not None

        self.fig_vel, self.ax_vel = plt.subplots()

        self.ax_vel.set_ylabel("Velocity")
        self.ax_vel.set_xlabel("Time")

        self.ax_vel.plot(self.body.pos[0], self.body.vel_norm)

        self.ax_vel.set_title(title)

    def save_plot_velocity(self, file_name: str = "body_velocity") -> None:
        if file_name[-4:] != ".pdf" and file_name[-4:] != ".png":
            file_name += ".pdf"
        self.fig_vel.savefig(file_name)


    # Global plot methods
    def show(self) -> None:
        plt.show()

    def clear_plots(self) -> None:
        self.fig = self.fig_ani = self.ax = self.ax_ani, self.fig_vel, self.ax_vel = None

    @abstractmethod
    def info(self) -> None:
        pass

    @staticmethod
    def _prt_info(coord_name: str, ordering: str, used: str, comment: str = None) -> None:
        print(f"{coord_name}:\n\t- Assumes ordering : <{ordering}> for state vectors but only <{used}> are used for plotting.")
        if comment is not None:
            print(f"\t- {comment}")


### BodyPlotter2D abstract class ###
# Class that facilitates the plotting of 2D Body objects.
class BodyPlotter2D(BodyPlotter):

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

    
### BodyPlotter3D abstract class ###
# Class that facilitates the plotting of 3D Body objects.
class BodyPlotter3D(BodyPlotter):

    def add_custom_surface(self, x: np.array, y: np.array, z: np.array, facecolor: str = 'k') -> None:
        if self.fig is not None: self.ax.plot_surface(x, y, z, color=facecolor, zorder=1)
        if self.fig_ani is not None: self.ax_ani.plot_surface(x, y, z, color=facecolor, zorder=1)

    def add_sphere(self, center: tuple[float, float], radius: float, facecolor: str) -> None:
        θ, φ = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
        x = radius * np.sin(θ) * np.cos(φ) + center[0]
        y = radius * np.sin(θ) * np.sin(φ) + center[1]
        z = radius * np.cos(θ) + center[2]
        self.add_custom_surface(x, y, z, facecolor=facecolor)


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


### BodyPlotter class ###
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
