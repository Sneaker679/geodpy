from .body import Body
from .coordinates import Coordinates, Cartesian, Spherical

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

### BodyPlotter class ###
# Class that facilitates the plotting of Body objects.
class BodyPlotter:
    
    # Parameter "dim" is the number of dimensions to plot (2 or 3)
    def __init__(self, body: Body, dim: int = 2) -> None:
        self.body = body
        self.coordinates = body._coordinates
        self.dim = 2

        self.fig, self.ax = None, None
        self.fig_ani, self.ax_ani = None, None
        self.fig_vel, self.ax_vel = None, None

        self.patches = []
        self.patches_ani = [] # Theses lists are always the same. Needed only because patches objects are unique to figures... Matplotlib flaw.

        self.ani = None


    # Orbit plotting methods
    def plot(self, title: str) -> None:
        self.fig = plt.figure()

        match self.coordinates.__qualname__:
            case Cartesian.__qualname__:
                if self.dim == 2:
                    self.ax = self.fig.add_subplot(111)
                    border = np.max(self.body.pos[1:3]) * 1.2
                    self.ax.set_ylim(-border, border)
                    self.ax.set_xlim(-border, border)
                    self.ax.plot(self.body.pos[1], self.body.pos[2])
                    self.ax.set_aspect(1)
                else: raise NotImplementedError

            case Spherical.__qualname__:
                if self.dim == 2:
                    self.ax = self.fig.add_subplot(111, projection="polar")
                    border = np.max(self.body.pos[1]) * 1.2
                    self.ax.set_ylim(0, border)
                    self.ax.plot(self.body.pos[3], self.body.pos[1])
                else: raise NotImplementedError

            case _:
                raise NotImplementedError

        self.ax.set_title(title)

        for patch in self.patches:
            patch.set(transform=self.ax.transData._b)
            self.ax.add_patch(patch)

    def save_plot(self, file_name: str = "body") -> None:
        if file_name[-4:-1] != ".pdf":
            file_name.join(".pdf")
        self.fig.savefig(file_name)


    # Animation plotting methods
    def animate(self, frame_interval: int = 20) -> None:
        self.fig_ani = plt.figure()

        border = np.max(self.body.pos[1]) * 1.2
        match self.coordinates.__qualname__:
            case Cartesian.__qualname__:
                if self.dim == 2:
                    self.ax_ani = self.fig_ani.add_subplot(111)
                    line = self.ax_ani.plot(self.body.pos[1], self.body.pos[2])[0]
                    self.ax_ani.set_xlim(-border, border)
                    self.ax_ani.set_ylim(-border, border)
                    self.ax_ani.set_aspect(1)
                else: raise NotImplementedError

            case Spherical.__qualname__:
                if self.dim == 2:
                    self.ax_ani = self.fig_ani.add_subplot(111, projection='polar')
                    line = self.ax_ani.plot(self.body.pos[3], self.body.pos[1])[0]
                    self.ax_ani.set_ylim(0, border)
                else: raise NotImplementedError

            case _: raise NotImplementedError

        for patch in self.patches_ani:
            patch.set(transform=self.ax_ani.transData._b)
            self.ax_ani.add_patch(patch)

        self.ani = animation.FuncAnimation(fig=self.fig_ani, func=self.__update_animation, save_count=self.body.pos.shape[1], interval=20, fargs=(line, ))

    def save_animation(self, file_name: str = "body") -> None:
        if file_name[-4:-1] != ".mp4":
            file_name.join(".mp4")
        self.ani.save(file_name)

    def __update_animation(self, frame, line):
        self.ax_ani.set_title(self.__update_title(frame))

        match self.coordinates.__qualname__:
            case Cartesian.__qualname__:
                if self.dim == 2:
                    x = self.body.pos[1][:frame]
                    y = self.body.pos[2][:frame]
                    line.set_xdata(x)
                    line.set_ydata(y)
                else: raise NotImplementedError

            case Spherical.__qualname__:
                if self.dim == 2:
                    r = self.body.pos[1][:frame]
                    φ = self.body.pos[3][:frame]
                    line.set_xdata(φ)
                    line.set_ydata(r)
                else: raise NotImplementedError

            case _: raise NotImplementedError

        return line

    def __update_title(self,frame: int) -> str:
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


    # Velocity plot methods
    def plot_velocity(self, title: str) -> None:
        assert self.body.vel_norm is not None

        self.fig_vel = plt.figure()
        self.ax_vel = self.fig_vel.add_subplot(111)

        self.ax_vel.set_ylabel("Velocity")
        self.ax_vel.set_xlabel("Time")

        self.ax_vel.plot(self.body.pos[0], self.body.vel_norm)

        self.ax_vel.set_title(title)

    def save_plot_velocity(self, file_name: str = "body_velocity") -> None:
        if file_name[-4:-1] != ".pdf":
            file_name.join(".pdf")
        self.fig_vel.savefig(file_name)


    # Global plot methods
    def show(self) -> None:
        plt.show()

    def set_patches(self, patches: list) -> None:
        import copy
        self.patches = patches
        self.patches_ani = copy.deepcopy(patches)


    def info_2Dcartesian(self, print_info: bool = False) -> None:
        self.__prt_info("2Dcartesian", "t x y z", "x y")

    def info_3Dcartesian(self, print_info: bool = False) -> None:
        self.__prt_info("3Dcartesian", "t x y z", "x y z")

    def info_polar(self, print_info: bool = False) -> None:
        self.__prt_info("Polar", "t r θ φ", "r φ", "Note: φ<0,2π>.")

    def info_spherical(self, print_info: bool = False) -> None:
        self.__prt_info("Spheric", "t r θ φ", "r θ φ", "Note: θ<0,π> and φ<0,2π>.")

    @staticmethod
    def __prt_info(coord_name: str, ordering: str, used: str, comment: str = None) -> None:
        print(f"{coord_name}:\n\t- Assumes ordering : <{ordering}> for state vectors but only <{used}> are used for plotting.")
        if comment is not None:
            print(f"\t- {comment}")
