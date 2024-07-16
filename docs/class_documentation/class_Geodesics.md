# class Geodesics
DESCRIPTION: Class that acts as a variable container for all geodesics-like variables.


## Parameters
- gₘₖ: `sympy.Matrix` ~~ Metric of the space-time with 4 dimensions.
- coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinate system used for calculation. Must match the coordinates already present in _gₘₖ.


## Attributes
- \_gₘₖ: `sympy.Matrix` ~~ Metric of the space-time with 4 dimensions.
- \_coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinate system used for calculation. Must match the coordinates already present in \_gₘₖ.
- \_dₛuᵏ: `sympy.Array[Function]` ~~ Symbolic acceleration vector for a body on a geodesic.
- \_dₛuᵏ\_lambda `list[typing.Callable]` ~~ Lambda acceleration vector for a body on a geodesic. Used for solving with scipy.integrate.solve\_ivp.


## Methods

#### def simplify()
DESCRIPTION: Simplifies the geodesics equations with Sympy if possible and stores the result in self.\_dₛuᵏ and self.\_dₛuᵏ\_lambda. Very performance hungry on big equations. 

RETURNS - None

PARAMETERS:
- None
