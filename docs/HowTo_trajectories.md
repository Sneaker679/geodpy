## Import
`geodpy` classes:
- `Geodesics`, `Body`.

`geodpy` functions:
- `expr_to_lambda`, `vector_to_lambda`.

Importable via &rarr `from geodpy import *`.

## Description
This is the most important of the *HowTo*s as we tacke the main purpose of this library - calculating trajectories of bodies in a given arbitrary metric. The 2 core objects are `Geodesics` and `Body`, who handle respectively the calculation of the symbolic geodesics and the calculation of the trajectories given the geodesics. All the results are stored in the attributes of these objects, such as all the points of a trajectory.

## Example
The main workflow for calculating trajectories looks like this:
- Defining the coordinate system and the metric;
- Calculating the symbolic geodesics from the metric;
- Calculating the trajectory of a body.
- Converting to cartesian/spheric

Let us go through each steps in more details. We will use the Kerr metric for this example, which corresponds to the space-time metric of a rotating blackhole.

### Defining the coordinate system
All space-time metrics are expressed in a particular coordinate system. For instance, the Minkowski metric, which represents a flat, gravity-less space-time, is usually represented in one of 2 ways: a cartesian system or spherical system. Respectively, they would look like this:
```math
\begin{align*} 
ds^2 &= dt^2 - dx^2 - dy^2 - dz^2 \\ 
ds^2 &= dt^2 - dr^2 - r^2 d\theta^2 - r^2 \sin^2 (\theta) d\phi^2
\end{align*}
```

The different systems yield a widely different form of the same metric. But from more complex metrics, more complex coordinate systems may emerge. As such, using the proper coordinate system becomes curcial to properly understand the results obtained when calculating a trajectory. More specifically, there is a need of converting a particular trajectory in a particular coordinate system into another coordinate system, like a cartesian system, which is easy to understand and plot using `matplotlib`. This is the job of the `Coordinates` subclasses of this library.

As of writing this, natively, geodpy supports 3 coordinate systems: `Cartesian`, `Spherical` and `OblongEllipsoid`. These can be imported via `from geodpy.coordinates import Cartesian, Spherical, OblongEllipsoid`. However, it is fairly easy to code yourself other coordinate systems and still be able to use the functionnalities of this library. For this, refer to the `HowTo_coordinates.md` file in this directory. 

The Kerr metric is represented in a OblongEllipsoid coordinate system. As such, we need to import this coordinate system and initialize the coordinates in order to declare the metric:
```python
from geodpy.coordinates import OblongEllipsoid
from sympy import *

rs = 1
a  = 0.2

t, r, θ, φ = OblongEllipsoid.coords
p2 = r*r + a*a*(cos(θ))**2 
Δ = r*r + a*a - r*rs
gₘₖ = Matrix([
    [1-rs*r/(p2)             ,0      ,0    ,(a*r*rs*sin(θ)**2)/(p2)                           ],
    [0                       ,-p2/Δ  ,0    ,0                                                 ],
    [0                       ,0      ,-p2  ,0                                                 ],
    [(a*r*rs*sin(θ)**2)/(p2) ,0      ,0    ,-(r*r + a*a + (a*a*r*rs*sin(θ)**2)/(p2))*sin(θ)**2]
])
```
This is the Kerr metric in oblong ellipsoid coordinates. In this particular example, "rs" and "a" are constants corresponding respectively to the Schwarzschild radius of the blackhole and its rotating speed. For physical reasons, a <= rs/2 must be true. 

## Calculating Geodesics
To calculate the geodesics, initialize a `Geodesics` object and feed it the metric and the coordinate system, like this:
```python
from geodpy import Geodesics

geodesics = Geodesics(OblongEllipsoid, gₘₖ)
```

The constructor of the object will automatically start computing the symbolic geodesics equations, as well as these equations as lambda expressions for later solving. Here, the geodesics equations are calculated using `∂ₛuᵏ = gᵐᵏ(∂ₛuₘ - ∂ₛgₘⱼuʲ)` where `uᵏ = ∂ₛxᵏ`, `∂ₛuⱼ = 1/2 * ∂ⱼ(gₘₖ) * uᵐ uᵏ` and `xᵏ` is a coordinate. Only the right side of the equation is stored and made into a lambda expression.

## Calculating the trajectory
Calculating trajectories require the use of a `Body` object. A body object is instantiated like so:
```python
initial_position = [..., ..., ..., ...]
initial_velocity = [..., ..., ..., ...]

body = Body(geodesics, initial_position, initial_velocity)
```

As you can see, the object needs to be fed its initial position and intial velocity. In other words, you need **8** initial values, otherwise the differential equation system cannot be resolved by the solver.

To solve the trajectory, run:
```python
s, pos, vel = body.solve_trajectory(time_interval=[0,100])
```
This method actually accepts many more parameters. Refer to the documentation of this particular class for more information. One thing to note is that the "time\_interval" parameter is not refering to coordinate time, but **proper time**, that is, the metric interval.

You can access the solved trajectory as was shown before, but these values are also stored in the attributes of the object. You can thus also do this once the `solve_trajectory()` method has been ran at least once:
```python
s, pos, vel = body.s, body.pos, body.vel
```

The solver being used in the background is from `scipy`. If you wish, you can access the complete results of the backend solver using:
```python
solver_result = body.solver_result
```

The solver is also capable of calculating the norm of the velocity vector for each point in time, assuming the first coordinate is coordinate time. To do so, run:
```python
vel_norm = body.calculate_velocities
```
which can also be accessed like this once the method has been ran at least once:
```python
vel_norm = body.vel_norm
```

## Converting the points to cartesian or spherical coordinates
To convert a body expressed in an arbitrary coordinate system to a cartesian or spherical system, you can use:
```python
cartesian_body = body.get_cartesian_body(a=0.2)
spheric_body = body.get_spheric_body(a=0.2)
```
These methods create new `Body` objects where the "pos" and "vel" attributes have been modified according to the new coordinate system. This step relies entirely on the implementation of the `Coordinates` class which was defined in the first step.

Also notice that these methods require the specification of the "a" parameter. This is because the `OblongEllipsoid` coordinate system is parametrized by "a", which corresponds in this case to the rotation speed of the blackhole. Other metrics may not need such parameters, in other words, the parameters of `get_x_body()` is metric dependant. See `HowTo_coordinates.md` for more information.

These new objects can now be used for plotting using the plotting functionalities of this library. Before the conversion, it was impossible to do so. Refer to `HowTo_plotters.md` to plot your body.
