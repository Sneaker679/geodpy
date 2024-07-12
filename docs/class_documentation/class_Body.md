# class Body
DESCRIPTION: Class responsible for solving the geodesic differential equation system and storing the results. The class can also calculate the norm of the velocity vector and convert itself to a cartesian or spherical coordinate system if given a properly implemented Coordinate system through the `Geodesics` object.


## Parameters
- geodesics: `geodpy.Geodesics` ~~ Geodesics object which contains the geodesics to solve through scipy.integrate.solve\_ivp.
- position\_vec: `list[float]` = [0,0,0,0] ~~ List containing the initial position values for the simulated body.
- velocity\_vec: `list[float]` = [0,0,0,0] ~~ List containing the initial velocity values for the simulated body. 

The values for each coordinate initial values needs to be in the same order as defined in the `Coordinates` object, which was passed to the `Geodesics` object upon instanciation beforehand. For example, for cartesian coordinates, that order would be : [t, x, y, z].


## Attributes
- \_geodesics: `geodpy.Geodesics` ~~ Geodesics object which contains the geodesics to solve through scipy.integrate.solve\_ivp.
- \_coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinates object for calculating the norm of the velocity vector, as well as converting the current coordinate base into a cartesian of spherical base.
- s: `numpy.array` ~~ Numpy array of the interval noted `s` for each point calculated using the `solve_trajectory()` method.
- pos: `numpy.array[numpy.array]` ~~ Numpy 2D array containing the position of the body at each point calculated using the `solve_trajectory()` method. Each row represents a coordinate and each column a different point that was solved.
- vel: `numpy.array[numpy.array]` ~~ Numpy 2D array containing the velocity of the body at each point calculated using the `solve_trajectory()`. Each row represents a coordinate and each column the velocity of a specific point that was solved.
- vel\_norm: `numpy.array` ~~ Numpy array which contains the norm of the velocity vector for each point in the `pos` attribute. This array is equal to `None` until the calculate\_velocities method was ran by the user.
- solver\_result: `scipy.integrate._ivp.ivp.OdeResult` ~~ Complete result yielded by the scipy.integrate.solve\_ivp function, which is used by the `solve_trajectory()` method.


## Methods


### def solve\_trajectory()
DESCRIPTION: This function takes the initial position and velocity of the body and calculates its trajectory according to the geodesics provided upon instanciating the object.

RETURNS - s, pos, vel: `np.array` ~~ Interval (proper time), position and velocity of the body for many points. The result is also stored in self.s, self.pos and self.vel

PARAMETERS:
- time\_interval: `tuple[float, float]` ~~ Interval of the interval... (proper time) for solving.
- method: `str` = 'Radau' ~~ Solver algorithm used by the solver. This is fed directly to scipy.integrate.solve\_ivp.
- max\_step: `float` = 1 ~~ Max interval (proper time) step. Higher values will yield less precise results.
- atol: `float` = 1e-8 ~~ Maximum absolute tolerance for error mitigation.
- rtol: `float` = 1e-8 ~~ Maximum relative tolerance for error mitigation.
- events: `typing.Callable` = None ~~ Function to be ran by the solver at each step. See scipy's documentation.


#### def calculate\_velocities()
DESCRIPTION: Calculates the norm of the velocity vector for each point of the trajectory using its position as a function of time. This function assumes that self.pos[0] is coordinate time and the resulting velocities are function of that time, not the interval. The results are stores in self.vel\_norm.

RETURNS - vel\_norm: `np.array` ~~ Norm of the velocity vector for each point of the trajectory.

PARAMETERS:
- None


#### def get\_cartesian\_body()
DESCRIPTION: Transforms the self.pos and self.vel attributes from its current coordinate system to a cartesian coordinate system by creating an entirely new body object. Highly dependant on the `Coordinates` static class fed to the `Body` object through the `Geodesics` object when instantiating.

RETURNS - new\_body: `geodpy.Body` ~~ New body with no geodesics tied to it. The only set attributes are self.\_coordinates, self.s and self.pos which now correspond to the new cooridnate system.

PARAMETERS:
 - \*\*kwargs ~~ Arguments to be given to the `to_cartesian()` method of `self._coordinates` as a parameter for conversion. Some coordinate systems require these additionnal arguments. For instance, the OblongElipsoid system requires the parameter `a`, which corresponds to how much "Oblong" the geometry is. When `a = 0`, we get a spheric coordinate system.


#### def get\_spheric\_body()
DESCRIPTION: Transforms the self.pos and self.vel attributes from its current coordinate system to a spheric coordinate system by creating an entirely new body object. Highly dependant on the `Coordinates` static class fed to the `Body` object through the `Geodesics` object when instantiating.

RETURNS - new\_body: `geodpy.Body` ~~ New body with no geodesics tied to it. The only set attributes are self.\_coordinates, self.s and self.pos which now correspond to the new cooridnate system.

PARAMETERS:
 - \*\*kwargs ~~ Arguments to be given to the `to_spherical()` method of `self._coordinates` as a parameter for conversion. Some coordinate systems require these additionnal arguments. For instance, the OblongElipsoid system requires the parameter `a`, which corresponds to how much "Oblong" the geometry is. When `a = 0`, we get a spheric coordinate system.



