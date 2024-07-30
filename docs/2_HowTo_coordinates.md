## Import
`geodpy.coordinates` classes:
- (ABSTRACT) `Coordinates`;
- `Cartesian`, `Spherical`, `OblongEllipsoid`, `LeMaitre`.

Importable via: `from geodpy.plotters import *`.

## Description
The `Coordinates` classes are responsible for handling all the coordinates in the library, including conversions between different coordinate systems. The 2 main objects using the `Coordinates` objects are `geodpy.Geodesics` and `geodpy.Body`. These are **static** classes.

The `Coordinates` classes are especially useful for handling conversions between coordinate systems. For instance, if you have calculated a particular trajectory with an arbitrary metric, this metric may not be expressed in standard cartesian or spherical coordinates, and so you might need a way to convert your trajectory data into one of these 2 coordinate systems which are easy to visualize. This conversion is made easy through this implementation.

## Example
The usage of the `Coordinates` is already presented in the `HowTo_trajectories.md` of the previous directory. Let us look instead at how one would define his own `Coordinates` class to accommodate a custom metric.

First, import the abstract `Coordinates` class and start coding a new class with `Cordinates` as the parent class. It should look like this, given the arbitrary coordinates [coord0, coord1, coord2, coord3]:
```python
from geodpy.coordinates import Coordinates

class Custom_System(Coordinates):
    interval: Symbol               = symbols('s')
    coords: tuple[Function]        = (Function('coord0')(interval), Function('coord1')(interval), Function('coord2')(interval), Function('coord3')(interval))
    coords_string: tuple[str]      = ('coord1', 'coord2', 'coord2', 'coord3')
    coord0, coord1, coord2, coord3 = coords

    @classmethod
    def velocity_equation(cls, a: float) -> Function:
        ...

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        ...

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        ...
```

You may replace the coord*x* variables by something more appropriate. If you need to calculate the velocity of a body using this library, you can hardcode the "velocity\_equation" into the method of the same name. The equation needs to be a sympy `Function` object corresponding to the velocity formula for that particular system. Of course, you need to use the coordinates already defined within the class. To do so, the method `velocity_equation()` has been decorated with `@classmethod` so that you can access the class variables with the identifier "cls".

The code will then use this symbolic expression to calculate the velocity as a function of the coordinate time (coord0). NOTE: Although the coordinates are sympy functions of the **interval** (proper time), the code will later assume these coordinates are actually functions of **coordinate time** to calculate the velocity, so don't concern yourself with the parametrization of this equation.

The next step is to define the transformation to a cartesian and spherical system. We want to be able to convert an array of points expressed in an arbitrary coordinate system and convert it in a cartesian or spherical coordinate system, which is more conveniant to use. Let us take a look at the OblongEllipsoid coordinate system which is already coded into the library:
```
class OblongEllipsoid(Coordinates):
    interval: Symbol            = symbols('s')
    coords: tuple[Function]     = (Function('t')(interval), Function('r')(interval), Function('θ')(interval), Function('φ')(interval))
    coords_string: tuple[str]   = ('t', 'r', 'θ', 'φ')
    t, r, θ, φ                  = coords

    @classmethod
    def velocity_equation(cls, **kwargs) -> Function:
        a = kwargs.get('a',0)
        return ( cls.r.diff(cls.interval)**2 * (sin(cls.θ)**2 * cls.r**2/(cls.r**2 + a**2) + cos(cls.θ)**2) + cls.r**2 * cls.θ.diff(cls.interval)**2 + cls.r**2 * cls.φ.diff(cls.interval)**2 * sin(cls.θ)**2 + a**2 * (cls.θ.diff(cls.interval)**2 * cos(cls.θ)**2 + cls.φ.diff(cls.interval)**2 * sin(cls.θ)**2) )**(1/2)

    def to_cartesian(pos: np.array, **kwargs) -> np.array:
        a = kwargs.get('a',0)

        r, θ, φ = pos[1:4]

        sinθ = np.sin(θ)

        x = np.sqrt(r*r + a*a) * sinθ * np.cos(φ)
        y = np.sqrt(r*r + a*a) * sinθ * np.sin(φ)
        z = r * np.cos(θ)

        return np.array([pos[0], x, y, z])

    def to_spherical(pos: np.array, **kwargs) -> np.array:
        a = kwargs.get('a',0)

        r, θ = pos[1:3]

        sinθ = np.sin(θ)

        r_sp = np.sqrt(r*r + a*a*sinθ*sinθ)
        θ_sp = np.arctan(np.sqrt(1+a*a/(r*r))*np.tan(θ))

        return np.array([pos[0], r_sp, θ_sp, pos[3]])
```

In this example, the `to_cartesian()` and `to_spherical()` methods have been redefined to accomodate this particular coordinate system. They take as input a numpy array of **points** that we assume are expressed in a oblong ellipsoid coordinate system. The conversion to cartesian/spherical is then handled by simple formulas, and the output is a numpy array of points, but this time expressed in the new coordinate system. However, notice how these methods are parametrized by a \*\*kwargs dictionnary. In this specific method, we require the parameter "a", which corresponds to how *squished* the ellipsoid is. As you may have realized, these kwargs are specific to the coordinate system, as in a system may be parametrized by other values. Be mindful of that when implementating your own coordinate system.

The `velocity_equation` was also redefined and returns, as stated before, the velocity equation for this particular coordinate system. It is also parametrized by "a". Using polymorphism, the code will call the proper method to calculate the velocity.

Using this strategy, you can easily test many metrics in abitrary coordinate systems while still using the tools of this library.
