# class BodyPlotter3D(BodyPlotter) <-- Abstract class
DESCRIPTION: Abstract class for all 2D plotters. Adds some methods for adding shapes onto the plot.


## Parameters
Parent parameters


## Attributes
Parent Attributes


## Methods


### add\_custom\_surface()
DESCRIPTION: Add a custom surface to the trajectory plots.

RETURNS - None

#### Parameters
- x: `np.array` ~~ Array of the x coordinates of a single point to draw.
- y: `np.array` ~~ Array of the y coordinates of a single point to draw.
- z: `np.array` ~~ Array of the z coordinates of a single point to draw.
- facecolor: `str` = 'k' ~~ Color of the surface. Has no effect if fill = False.


### add\_sphere()
DESCRIPTION: Add a sphere to the trajectory plots.

RETURNS - None

PARAMETERS:
- center: `tuple[float, float]` ~~ Coordinates of the center of the sphere.
- radius: `float` ~~ Radius of the sphere.
- facecolor: `str` ~~ Color of the face of the sphere.
