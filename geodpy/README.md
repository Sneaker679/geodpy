# Interface of classes

## class Coordinates(metaclass=ABCMeta) <-- Abstract class
DESCRIPTION: Abstract and static class that all coordinates systems need to be derived from for this code to work.


### Parameters
None


### Attributes
- interval: `sympy.Symbol` ~~ Sympy Symbol to be used to represent the space-time interval, like proper time.
- coords: `tuple[sympy.Function]` ~~ List of all the coordinates of this coordinate system. These coordinates are sympy functions that are dependant on the interval (previous attribute).
- coords\_string: `tuple[str]` ~~ String representation of the coordinates for printing purposes.
- velocity\_equation: `sympy.Function` ~~ Sympy Function that sets how to calculate the norm of the velocity vector for this particular coordinate system.


### Methods


#### def to\_cartesian()
DESCRIPTION: Takes a 2D array of values that are presumed in a specific coordinate system and returns the 2D array of these values in a cartesian system.

RETURNS - new\_values: np.array ~~ Array of values expressed in a cartesian system.

##### Parameters
- pos: np.array ~~ 2D numpy array of values to convert.
- \*\*kwargs ~~ Additionnal arguments needed for the conversion. Depends on the coordinate system.


#### def to\_spherical()
DESCRIPTION: Takes a 2D array of values that are presumed in a specific coordinate system and returns the 2D array of these values in a spherical system.

RETURNS - new\_values: np.array ~~ Array of values expressed in a spherical system.

##### Parameters
- pos: np.array ~~ 2D numpy array of values to convert.
- \*\*kwargs ~~ Additionnal arguments needed for the conversion. Depends on the coordinate system.


## class Cartesian(Coordinates (<-- parent class))
DESCRIPTION: Child class of `Coordinates` which implements a cartesian coordinate system.


### Attributes
- Parent class attributes
- t: `sympy.Function` ~~ Unpacked time `Function` from self.coords
- x: `sympy.Function` ~~ Unpacked x `Function` from self.coords
- y: `sympy.Function` ~~ Unpacked y `Function` from self.coords
- z: `sympy.Function` ~~ Unpacked z `Function` from self.coords


### Methods
Parent class methods




## class OblongEllipsoid(Coordinates)
DESCRIPTION: Child class of `Coordinates` which implements a OblongEllipsoid coordinate system.


### Attributes
- Parent class attributes
- t: `sympy.Function` ~~ Unpacked time `Function` from self.coords
- x: `sympy.Function` ~~ Unpacked x `Function` from self.coords
- θ: `sympy.Function` ~~ Unpacked y `Function` from self.coords
- φ: `sympy.Function` ~~ Unpacked z `Function` from self.coords


### Methods
Parent class methods




## class Spherical(Coordinates, OblongEllipsoid)
DESCRIPTION: Child class of `Coordinates` which implements a cartesian coordinate system.


### Attributes
- Parent class attributes


### Methods
Parent class methods




## class Geodesics
DESCRIPTION: Class that acts as a variable container for all geodesics-like variables.


### Parameters
- gₘₖ: `sympy.Matrix` ~~ Metric of the space-time with 4 dimensions.
- coordinates: `geodpy.Coordinates` ~~ Coordinate system used for calculation. Must match the coordinates already present in _gₘₖ.


### Attributes
- \_gₘₖ: `sympy.Matrix` ~~ Metric of the space-time with 4 dimensions.
- \_coordinates: `geodpy.Coordinates` ~~ Coordinate system used for calculation. Must match the coordinates already present in \_gₘₖ.
- \_dₛuᵏ: `sympy.Array[Function]` ~~ Symbolic acceleration vector for a body on a geodesic.
- \_dₛuᵏ\_lambda `list[typing.Callable]` ~~ Lambda acceleration vector for a body on a geodesic. Used for solving with scipy.integrate.solve\_ivp.


### Methods
No public methods.




## class Body
DESCRIPTION: Class responsible for solving the geodesic differential equation system and storing the results. The class can also calculate the norm of the velocity vector and convert itself to a cartesian or spherical coordinate system if given a properly implemented Coordinate system through the `Geodesics` object.


### Parameters
- geodesics: `geodpy.Geodesics` ~~ Geodesics object which contains the geodesics to solve through scipy.integrate.solve\_ivp.
- position\_vec: `list[float]` = [0,0,0,0] ~~ List containing the initial position values for the simulated body.
- velocity\_vec: `list[float]` = [0,0,0,0] ~~ List containing the initial velocity values for the simulated body. 

The values for each coordinate initial values needs to be in the same order as defined in the `Coordinates` object, which was passed to the `Geodesics` object upon instanciation beforehand. For example, for cartesian coordinates, that order would be : [t, x, y, z].


### Attributes
- \_geodesics: `geodpy.Geodesics` ~~ Geodesics object which contains the geodesics to solve through scipy.integrate.solve\_ivp.
- \_coordinates: `geodpy.Coordinates` ~~ Coordinates object for calculating the norm of the velocity vector, as well as converting the current coordinate base into a cartesian of spherical base.
- s: `numpy.array` ~~ Numpy array of the interval noted `s` for each point calculated using the `solve_trajectory()` method.
- pos: `numpy.array[numpy.array]` ~~ Numpy 2D array containing the position of the body at each point calculated using the `solve_trajectory()` method. Each row represents a coordinate and each column a different point that was solved.
- vel: `numpy.array[numpy.array]` ~~ Numpy 2D array containing the velocity of the body at each point calculated using the `solve_trajectory()`. Each row represents a coordinate and each column the velocity of a specific point that was solved.
- vel\_norm: `numpy.array` ~~ Numpy array which contains the norm of the velocity vector for each point in the `pos` attribute. This array is equal to `None` until the calculate\_velocities method was ran by the user.
- solver\_result: `scipy.integrate._ivp.ivp.OdeResult` ~~ Complete result yielded by the scipy.integrate.solve\_ivp function, which is used by the `solve_trajectory()` method.


### Methods


#### def solve\_trajectory()
DESCRIPTION: This function takes the initial position and velocity of the body and calculates its trajectory according to the geodesics provided upon instanciating the object.

RETURNS - s, pos, vel: `np.array` ~~ Interval (proper time), position and velocity of the body for many points. The result is also stored in self.s, self.pos and self.vel

##### Parameters
- time\_interval: `tuple[float, float]` ~~ Interval of the interval... (proper time) for solving.
- method: `str` = 'Radau' ~~ Solver algorithm used by the solver. This is fed directly to scipy.integrate.solve\_ivp.
- max\_step: `float` = 1 ~~ Max interval (proper time) step. Higher values will yield less precise results.
- atol: `float` = 1e-8 ~~ Maximum absolute tolerance for error mitigation.
- rtol: `float` = 1e-8 ~~ Maximum relative tolerance for error mitigation.
- events: `typing.Callable` = None ~~ Function to be ran by the solver at each step. See scipy's documentation.


#### def calculate\_velocities()
DESCRIPTION: Calculates the norm of the velocity vector for each point of the trajectory using its position as a function of time. This function assumes that self.pos[0] is coordinate time and the resulting velocities are function of that time, not the interval. The results are stores in self.vel\_norm.

RETURNS - vel\_norm: `np.array` ~~ Norm of the velocity vector for each point of the trajectory.

##### Parameters
None


#### def get\_cartesian\_body()
DESCRIPTION: Transforms the self.pos and self.vel attributes from its current coordinate system to a cartesian coordinate system by creating an entirely new body object. Highly dependant on the `Coordinates` static class fed to the `Body` object through the `Geodesics` object when instantiating.

RETURNS - new\_body: `geodpy.Body` ~~ New body with no geodesics tied to it. The only set attributes are self.\_coordinates, self.s and self.pos which now correspond to the new cooridnate system.

##### Parameters
 - \*\*kwargs ~~ Arguments to be given to the `to_cartesian()` method of self.`_coordinates ` as a parameter for conversion. Some coordinate systems require these additionnal arguments. For instance, the OblongElipsoid system requires the parameter `a`, which corresponds to how much "Oblong" the geometry is. When `a = 0`, we get a spheric coordinate system.


#### def get\_spheric\_body()
DESCRIPTION: Transforms the self.pos and self.vel attributes from its current coordinate system to a spheric coordinate system by creating an entirely new body object. Highly dependant on the `Coordinates` static class fed to the `Body` object through the `Geodesics` object when instantiating.

RETURNS - new\_body: `geodpy.Body` ~~ New body with no geodesics tied to it. The only set attributes are self.\_coordinates, self.s and self.pos which now correspond to the new cooridnate system.

##### Parameters
 - \*\*kwargs ~~ Arguments to be given to the `to_spherical()` method of self.`_coordinates ` as a parameter for conversion. Some coordinate systems require these additionnal arguments. For instance, the OblongElipsoid system requires the parameter `a`, which corresponds to how much "Oblong" the geometry is. When `a = 0`, we get a spheric coordinate system.




## class BodyPlotter(metaclass=ABCMeta) <-- Abstract class
DESCRIPTION: Automates the plotting of `Body` trajectories with `matplotlib`.


### Parameters
- body: `geodpy.Body` ~~ Body object to be plotted.


### Attributes
- body: `geodpy.Body` ~~ Body object to be plotted.
- coordinates: `geodpy.Coordinates` ~~ Coordinates to be used for plotting. This basically only affect the title of the animation produced as it fetches the string representation of the coordinates.
- fig, fig\_ani and fig\_vel: `matplotlib.figure.Figure` ~~ Attributes containing the `Figure` instances of matplotlib for each the graphs. One for the orbit, one for the animation of the orbit and one for the velocity.
- ax, ax\_ani and ax\_vel: `matplotlib.axes.Axes` ~~ Attributes containing the `Axes` instances of matplotlib for each the graphs. One for the orbit, one for the animation of the orbit and one for the velocity.
- ani: `matplotlib.animation.Animation` ~~ Attribute containing the `Animation` instance of matplotlib.


### Methods


#### def plot()
DESCRIPTION: Plots the trajectory from the data in self.body.

RETURNS - None

##### Parameters
 - title: `str` ~~ Title of the plot.


#### def save\_plot()
DESCRIPTION: Saves the trajectory plot.

RETURNS - None

##### Parameters
- file\_name: `str` = "body" ~~ Name of the saved file.


#### def animate()
DESCRIPTION: Animates the trajectory from the data in self.body.

RETURNS - None

##### Parameters
- frame\_interval: `int` = 20 ~~ Frame interval between animation frames.


#### def save\_animation()
DESCRIPTION: Saves the animation of the trajectory as a mp4 file.

RETURNS - None

##### Parameters
- file\_name: `str` = "body" ~~ Name of the saved file.
- dpi: `int` = 100 ~~ Number of dots per inch. 


#### def plot\_velocity()
DESCRIPTION: Plots the norm velocity vector as a function of time from the data in self.body.

RETURNS - None

##### Parameters
- title: `str` ~~ Title of the plot.


#### def save\_plot()
DESCRIPTION: Saves the velocity plot.

RETURNS - None

##### Parameters
- file\_name: `str` = "body\_velocity" ~~ Name of the saved file.


#### def show()
DESCRIPTION: Shows all plotted plots.

RETURNS - None

##### Parameters
None


#### def clear\_plots()
DESCRIPTION: Clears all the plots, almost effectively resetting the object.

RETURNS - None

##### Parameters
None


#### def info()
DESCRIPTION: Prints information on what assumptions were made for plotting.
RETURNS - None

##### Parameters
None




## class BodyPlotter2D(BodyPlotter) <-- Abstract class
DESCRIPTION: Abstract class for all 2D plotters. Adds some methods for adding shapes onto the plot.


### Parameters
Parent parameters


### Attributes
Parent Attributes


### Methods
#### add\_custom\_patches()
DESCRIPTION: Add custom matplotlib patches to the trajectory plots.

RETURNS - None

##### Parameters
- \*argv: `matplotlib.patches.Patch` ~~ Patches to add to the plots.


#### add\_circle()
DESCRIPTION: Add a circle patch to the trajectory plots.

RETURNS - None

##### Parameters
- center: `tuple[float, float]` ~~ Coordinates of the center of the circle.
- radius: `float` ~~ Radius of the circle.
- edgecolor: `str` ~~ Color of the edge of the circle.
- facecolor: `str` = None ~~ Color of the face of the circle. Has no effect if fill = False.
- fill: `bool` = False ~~ Whether to fill the circle or not. 




## class BodyPlotter3D(BodyPlotter) <-- Abstract class
DESCRIPTION: Abstract class for all 2D plotters. Adds some methods for adding shapes onto the plot.


### Parameters
Parent parameters


### Attributes
Parent Attributes


### Methods


#### add\_custom\_surface()
DESCRIPTION: Add a custom surface to the trajectory plots.

RETURNS - None

##### Parameters
- x: `np.array` ~~ Array of the x coordinates of a single point to draw.
- y: `np.array` ~~ Array of the y coordinates of a single point to draw.
- z: `np.array` ~~ Array of the z coordinates of a single point to draw.
- facecolor: `str` = 'k' ~~ Color of the surface. Has no effect if fill = False.


#### add\_sphere()
DESCRIPTION: Add a sphere to the trajectory plots.

RETURNS - None

##### Parameters
- center: `tuple[float, float]` ~~ Coordinates of the center of the sphere.
- radius: `float` ~~ Radius of the sphere.
- facecolor: `str` ~~ Color of the face of the sphere.




## class CartesianPlot2D(BodyPlotter2D, BodyPlotter)
DESCRIPTION: 2D Cartesian plotter. The `Coordinates` of `Body` must be `Cartesian`.


### Parameters
Parent `BodyPlotter` parameters.


### Attributes
Parent `BodyPlotter` parameters.


### Methods
Parents methods.




## class CartesianPlot3D(BodyPlotter3D, BodyPlotter)
DESCRIPTION: 3D Cartesian plotter. The `Coordinates` of `Body` must be `Cartesian`.


### Parameters
Parent `BodyPlotter` parameters.


### Attributes
Parent `BodyPlotter` parameters.


### Methods
Parents methods.




## class PolarPlot(BodyPlotter2D, BodyPlotter)
DESCRIPTION: 2D Spherical plotter (Polar plotter). The `Coordinates` of `Body` must be `Spherical`.


### Parameters
Parent `BodyPlotter` parameters.


### Attributes
Parent `BodyPlotter` parameters.


### Methods
Parents methods.




# Functions
## def basic()
DESCRIPTION: Takes in basic parameters and automates the process of taking a metric to plot geodesics. 

RETURNS - body: `geodpy.Body` ~~ A body containing a fully solved trajectory.

### Parameters
- coordinates: `geodpy.Coordinates` ~~ Coordinate system to be used.
- g\_mk: `sympy.Matrix` ~~ Metric of the space-time. Needs to use the same coordinates as self.coordinates.
- initial\_pos: `list[float]` ~~ Initial position of the object to be fed to the `Body` object.
- initial\_vel: `list[float]` ~~ Initial velocity of the object to be fed to the `Body` object.
- solver\_kwargs: `dict` = {} ~~ Arguments of the `body.solve\_trajectory()` method. If the dictionnary is missing arguments, it defaults to hard coded values. 
- verbose: `int` ~~ Describes how verbose the output should be. Currently, only verbose=2 actually currates the printing amount. The verbose=1 situation is left for functions that would use `basic()` as an intermediary while keeping the same verbose variable.


## expr\_to\_lambda()
DESCRIPTION: Takes a sympy `Function` object and converts it to a lambda function. This is not meant to be used outside this project's, as it assumes many things.

RETURNS - lambda: typing.Callable ~~ Lambda function to be used for numerical solving.

### Parameters
- coordinates: `geodpy.Coordinates` ~~ Coordinates system to be used for the conversion of the expression.
- expression: `sympy.Function` ~~ Expression to be converted.


## vector\_to\_lambda()
DESCRIPTION: Takes a sympy `Array` object (more specifically, `Array` of `Function`) and converts it to a list of lambda functions.

RETURNS - lambda\_list: `list[typing.Callable]` ~~ List of lambda functions to be used for numerical computing.

### Parameters
- coordinates: `geodpy.Coordinates` ~~ Coordinates system to be used for the conversion of the array of expressions.
- expressions: `sympy.Array` ~~ Array of functions to convert.
