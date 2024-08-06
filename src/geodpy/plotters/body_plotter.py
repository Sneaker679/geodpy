from .. import Body

from sympy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from abc import ABCMeta, abstractmethod

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
