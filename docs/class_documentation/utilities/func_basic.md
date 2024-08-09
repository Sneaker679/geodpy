# def basic()
DESCRIPTION: Takes in basic parameters and automates the process of taking a metric to plot geodesics. 

RETURNS - body: `geodpy.Body` ~~ A body containing a fully solved trajectory.

PARAMETERS
- coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinate system to be used.
- g\_mk: `sympy.Matrix` ~~ Metric of the space-time. Needs to use the same coordinates as self.coordinates.
- initial\_pos: `list[float]` ~~ Initial position of the object to be fed to the `Body` object.
- initial\_vel: `list[float]` ~~ Initial velocity of the object to be fed to the `Body` object.
- solver\_kwargs: `dict` = {} ~~ Arguments of the `body.solve\_trajectory()` method. If the dictionnary is missing arguments, it defaults to hard coded values. 
- verbose: `int` ~~ Describes how verbose the output should be. Currently, only verbose=2 actually currates the printing amount. The verbose=1 situation is left for functions that would use `basic()` as an intermediary while keeping the same verbose variable.
