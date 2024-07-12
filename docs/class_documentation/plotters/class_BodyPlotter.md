# class BodyPlotter(metaclass=ABCMeta) <-- Abstract class
DESCRIPTION: Automates the plotting of `Body` trajectories with `matplotlib`.


## Parameters
- body: `geodpy.Body` ~~ Body object to be plotted.


## Attributes
- body: `geodpy.Body` ~~ Body object to be plotted.
- coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinates to be used for plotting. This basically only affect the title of the animation produced as it fetches the string representation of the coordinates.
- fig, fig\_ani and fig\_vel: `matplotlib.figure.Figure` ~~ Attributes containing the `Figure` instances of matplotlib for each the graphs. One for the orbit, one for the animation of the orbit and one for the velocity.
- ax, ax\_ani and ax\_vel: `matplotlib.axes.Axes` ~~ Attributes containing the `Axes` instances of matplotlib for each the graphs. One for the orbit, one for the animation of the orbit and one for the velocity.
- ani: `matplotlib.animation.Animation` ~~ Attribute containing the `Animation` instance of matplotlib.


## Methods


### def plot()
DESCRIPTION: Plots the trajectory from the data in self.body.

RETURNS - None

PARAMETERS:
 - title: `str` ~~ Title of the plot.


### def save\_plot()
DESCRIPTION: Saves the trajectory plot.

RETURNS - None

PARAMETERS:
- file\_name: `str` = "body" ~~ Name of the saved file.


### def animate()
DESCRIPTION: Animates the trajectory from the data in self.body.

RETURNS - None

PARAMETERS:
- frame\_interval: `int` = 20 ~~ Frame interval between animation frames.


### def save\_animation()
DESCRIPTION: Saves the animation of the trajectory as a mp4 file.

RETURNS - None

PARAMETERS:
- file\_name: `str` = "body" ~~ Name of the saved file.
- dpi: `int` = 100 ~~ Number of dots per inch. 


### def plot\_velocity()
DESCRIPTION: Plots the norm velocity vector as a function of time from the data in self.body.

RETURNS - None

PARAMETERS:
- title: `str` ~~ Title of the plot.


### def save\_plot\_velocity()
DESCRIPTION: Saves the velocity plot.

RETURNS - None

PARAMETERS
- file\_name: `str` = "body\_velocity" ~~ Name of the saved file.


### def show()
DESCRIPTION: Shows all plotted plots.

RETURNS - None

PARAMETERS:
- None


### def clear\_plots()
DESCRIPTION: Clears all the plots, almost effectively resetting the object.

RETURNS - None

PARAMETERS:
- None


### def info()
DESCRIPTION: Prints information on what assumptions were made for plotting.

RETURNS - None

PARAMETERS:
- None
