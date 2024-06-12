from body import Body

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

class BodyPlotter:
    
    def __init__(self, body: Body) -> None:
        self.body = body
        self._coordinate_type = "2Dcartesian"
        self._coordinate_string = ['t', 'x', 'y', 'z']
        self.fig, self.ax = None, None
        self.fig_ani, self.ax_ani = None, None
        self.ani = None


    def plot(self, title: str, patches = []) -> None:
        if self._coordinate_type in ["2Dcartesian", "polar"]:
            self.fig = plt.figure()
            match self._coordinate_type:
                case "2Dcartesian":
                    self.ax = self.fig.add_subplot(111)
                    border = np.max(self.body.pos[1:3]) * 1.2
                    self.ax.set_ylim(-border, border)
                    self.ax.set_xlim(-border, border)
                    self.ax.plot(self.body.pos[1], self.body.pos[2])

                case "polar":
                    self.ax = self.fig.add_subplot(111, projection="polar")
                    border = np.max(self.body.pos[1]) * 1.2
                    self.ax.set_ylim(0, border)
                    self.ax.plot(self.body.pos[3], self.body.pos[1])

                case _:
                    raise NotImplementedError

        else:
            raise NotImplementedError

        self.ax.set_title(title)

        for patch in patches:
            self.ax.add_patch(patch)

    def save_plot(self, file_name: str = "body") -> None:
        if file_name[-4:-1] != ".pdf":
            file_name.join(".pdf")
        self.fig.savefig(file_name)


    def animate(self, patches = []) -> None:
        self.fig_ani = plt.figure()

        border = np.max(self.body.pos[1]) * 1.2
        match self._coordinate_type:
            case "2Dcartesian":
                self.ax_ani = self.fig_ani.add_subplot(111)
                line = self.ax_ani.plot(self.body.pos[1], self.body.pos[2])[0]
                self.ax_ani.set_xlim(-border, border)
                self.ax_ani.set_ylim(-border, border)
            case "polar":
                self.ax_ani = self.fig_ani.add_subplot(111, projection='polar')
                line = self.ax_ani.plot(self.body.pos[3], self.body.pos[1])[0]
                self.ax_ani.set_ylim(0, border)
            case _:
                raise NotImplementedError

        for patch in patches:
            self.ax.add_patch(patch)

        self.ani = animation.FuncAnimation(fig=self.fig_ani, func=self.__update_animation, save_count=self.body.pos.shape[1], interval=20, fargs=(line, ))

    def save_animation(self, file_name: str = "body") -> None:
        if file_name[-4:-1] != ".mp4":
            file_name.join(".mp4")
        self.ani.save(file_name)

    def __update_animation(self, frame, line):
        self.ax_ani.set_title(self.__update_title(frame))

        match self._coordinate_type:
            case "2Dcartesian":
                x = self.body.pos[1][:frame]
                y = self.body.pos[2][:frame]
                line.set_xdata(x)
                line.set_ydata(y)

            case "polar":
                r = self.body.pos[1][:frame]
                φ = self.body.pos[3][:frame]
                line.set_xdata(φ)
                line.set_ydata(r)

            case _:
                raise NotImplementedError

        return line

    def __update_title(self,frame: int) -> str:
        s = '{:e}'.format(self.body.s[frame]),
        pos = [
            '{:e}'.format(self.body.pos[0][frame]),
            '{:e}'.format(self.body.pos[1][frame]),
            '{:e}'.format(self.body.pos[2][frame]),
            '{:e}'.format(self.body.pos[3][frame])
        ]

        title = f"s= {s},"
        for i, coord in enumerate(self._coordinate_string):
            title = ''.join([title, f" {coord}= {pos[i]}"])
            if i != 3:
                title = ''.join([title, ","])

        return title

    def show(self) -> None:
        plt.show()

    def set_2Dcartesian(self, print_info: bool = False) -> None:
        self._coordinate_type = "2Dcartesian"
        self._coordinate_string = ['t', 'x', 'y', 'z']
        if print_info is True:
            self.__prt_info(self._coordinate_type, "t x y z", "x y")

    def set_3Dcartesian(self, print_info: bool = False) -> None:
        self._coordinate_type = "3Dcartesian"
        self._coordinate_string = ['t', 'x', 'y', 'z']
        if print_info is True:
            self.__prt_info(self._coordinate_type, "t x y z", "x y z")

    def set_polar(self, print_info: bool = False) -> None:
        self._coordinate_type = "polar"
        self._coordinate_string = ['t', 'r', 'θ', 'φ']
        if print_info is True:
            self.__prt_info(self._coordinate_type, "t r θ φ", "r φ", "Note: φ<0,2π>.")

    def set_spherical(self, print_info: bool = False) -> None:
        self._coordinate_type = "spherical"
        self._coordinate_string = ['t', 'r', 'θ', 'φ']
        if print_info is True:
            self.__prt_info(self._coordinate_type, "t r θ φ", "r θ φ", "Note: θ<0,π> and φ<0,2π>.")

    @staticmethod
    def __prt_info(coord_name: str, ordering: str, used: str, comment: str = None) -> None:
        print(f"Plotting set to {coord_name}:\n\t- Assumes ordering : <{ordering}> for state vectors but only <{used}> are used for plotting.")
        if comment is not None:
            print(f"\t- {comment}")
