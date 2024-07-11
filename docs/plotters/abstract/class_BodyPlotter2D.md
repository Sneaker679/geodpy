# class BodyPlotter2D(BodyPlotter) <-- Abstract class
DESCRIPTION: Abstract class for all 2D plotters. Adds some methods for adding shapes onto the plot.


## Parameters
Parent parameters


## Attributes
Parent Attributes


## Methods
### add\_custom\_patches()
DESCRIPTION: Add custom matplotlib patches to the trajectory plots.

RETURNS - None

PARAMETERS:
- \*argv: `matplotlib.patches.Patch` ~~ Patches to add to the plots.


### add\_circle()
DESCRIPTION: Add a circle patch to the trajectory plots.

RETURNS - None

PARAMETERS:
- center: `tuple[float, float]` ~~ Coordinates of the center of the circle.
- radius: `float` ~~ Radius of the circle.
- edgecolor: `str` ~~ Color of the edge of the circle.
- facecolor: `str` = None ~~ Color of the face of the circle. Has no effect if fill = False.
- fill: `bool` = False ~~ Whether to fill the circle or not. 
