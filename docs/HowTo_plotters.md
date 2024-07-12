## Import
`geodpy.plotter` classes:
- (ABSTRACT) `BodyPlotter`;
- (ABSTRACT) `BodyPlotter2D`, `BodyPlotter3D`;
- (2D) `CartesianPlot2D`, `PolarPlot`;
- (3D) `CartesianPlot3D`.

Importable via: `from geodpy.plotters import *`.

## Description
These classes make it easier to plot on `matplotlib` the trajectory of `Body` objects expressed in `Cartesian` or `Spherical` coordinates.


## Example
A typical example for plotting would go as follows. We assume the variable "body" is a `Body` object and that its trajectory is already calculated and is expressed in a `Cartesian` coordinate system. For more info on this property of the `Body` class, see its documentation.

First, import the plotter and feed it the body object:
```python
# "body" is defined ...

from geodpy.plotters import CartesianPlot2D, CartesianPlot3D

plot_2D = CartesianPlot2D(body)
plot_3D = CartesianPlot3D(body)
```

To plot the trajectory, you can simply run:
```python
title = "trajectory"
plot_2D.plot(title) 
```

If you wish to animate that same trajectory, run:
```python
plot_2D.animate()
```

Finally, you can also plot the velocity of the object as a function of coordinate time. It is assumed that the first coordinate of your coordinate system is time. If you have not redefined any of the coordinate classes, you needn't worry about that. To plot the velocity, simply run:
```python
title = "v(t)"
plot_2D.plot_velocity(title) 
```

Now, to display all of these plots, simply run:
```python
plot_2D.show()
```

These classes also support adding shapes to the plot. For the 2D plotters, you can add custom `matplotlib.patches` instances to your plots and for the 3D plotters, you can add custom surfaces given a set of points. 

For this to work, your trajectories need to be plotted as shown earlier. Afterwords, for 2D plotters, you could run:
```python
circle1 = patches.Circle(center=(0,0), radius=1, edgecolor='k', facecolor='b', fill=True)
circle2 = patches.Circle(center=(1,0), radius=1, edgecolor='k', facecolor='b', fill=True)
circle3 = patches.Circle(center=(2,0), radius=1, edgecolor='k', facecolor='b', fill=True)
...
plot_2D.add_custom_patches(circle1, circle2, circle3, ...)
```
This will add N circles to your trajectory plots (that is, you trajectory plot and the animation plot).

For 3D plots, you can add surfaces instead. For example, in the kerr metric, you can add a Oblong Ellipsoid to represent the rotating blackhole:
```python
# "r_ext_oblong" is defined as the external horizon radius of the black hole
θ, φ = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
x = np.sqrt(r_ext_oblong**2 + a**2) * np.sin(θ) * np.cos(φ)
y = np.sqrt(r_ext_oblong**2 + a**2) * np.sin(θ) * np.sin(φ)
z = r_ext_oblong * np.cos(θ)
plotter.add_custom_surface(x, y, z)
```

More simply, you can also add basic shapes using this class' methods. For 2D plotters, you can easily add circles for instance:
```python
plot_2D.add_circle(center=(0,0), radius=5, edgecolor='k', facecolor='b', fill=True)
```
and for the 3D plotters, you can similarly add spheres:
```python
plot_3D.add_sphere(center=(0,0), radius=5, facecolor='b')
```

You can save your plots as PDFs using the following methods:
```
plot_2D.save_plot(file_name="plot")
plot_2D.save_animation(file_name="animation")
plot_2D.save_plot_velocity(file_name="velocity")
```

The `PolarPlot` class works in virtually the same way as what was already shown. Note that the polar plotting is strictly in 2 dimensions.
