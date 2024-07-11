# class Coordinates(metaclass=ABCMeta) <-- Abstract class
DESCRIPTION: Abstract and static class that all coordinates systems need to be derived from for this code to work.


## Parameters
None


## Attributes
- interval: `sympy.Symbol` ~~ Sympy Symbol to be used to represent the space-time interval, like proper time.
- coords: `tuple[sympy.Function]` ~~ List of all the coordinates of this coordinate system. These coordinates are sympy functions that are dependant on the interval (previous attribute).
- coords\_string: `tuple[str]` ~~ String representation of the coordinates for printing purposes.
- velocity\_equation: `sympy.Function` ~~ Sympy Function that sets how to calculate the norm of the velocity vector for this particular coordinate system.


## Methods


### def to\_cartesian()
DESCRIPTION: Takes a 2D array of values that are presumed in a specific coordinate system and returns the 2D array of these values in a cartesian system.

RETURNS - new\_values: np.array ~~ Array of values expressed in a cartesian system.

PARAMETERS
- pos: np.array ~~ 2D numpy array of values to convert.
- \*\*kwargs ~~ Additionnal arguments needed for the conversion. Depends on the coordinate system.


#### def to\_spherical()
DESCRIPTION: Takes a 2D array of values that are presumed in a specific coordinate system and returns the 2D array of these values in a spherical system.

RETURNS - new\_values: np.array ~~ Array of values expressed in a spherical system.

PARAMETERS
- pos: np.array ~~ 2D numpy array of values to convert.
- \*\*kwargs ~~ Additionnal arguments needed for the conversion. Depends on the coordinate system.

