# geodpy
This code aims to facilitate research on dark matter by simulating any geodesics given a metric specified by the user and some initial conditions.

## Requirements
- matplotlib
- sympy
- scipy
- numpy

## Installation
Add the `darkMatter` folder to your directory by adding this line to your .basrc or .zshrc file:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/darkMatter/"
```
or simply run it once, directly in the terminal for single use cases.

## Basic Usage
In the `examples` folder are many examples that simulate geodesics with varied metrics, including the Schwarzschild, Kerr and Schwarzschild de Sitter metric. All these folders work in the same way. Thus, for the sake of being straightforward, I shall present only one example with the Schwarzschild metric. Inside the `schwarzschild` folder are many files, the main one being `schwarzschild.py`. This file contains the bulk of the code specific to running a schwarzchild metric calculation. Inside this code, there is a `schwarzschild()` function, which you can call with varying parameters to generate different geodesics. The other files in the `schwarzschild` folder are simple sripts who call the `schwarzschild()` function with different initial values. For instance, the `near_horizon.py` script yields a geodesic simulated near the event horizon of a non rotating Schwarzschild blackhole. Running this script using `python3 near_horizon.py` will run the entire calculation and plotting code with no extra steps needed. You can run the other examples the same way. The README inside each example folders specifies the meaning of the constants and quantities used. 

## Advanced Usage
Seeing as you have added the project folder to your python path, you can call the classes and functions of this code from any location in your computer. Once you have established a workspace, create an empty scrip and start coding!

The basic strategy to yield results is described below.

#### 0. Hold on!
Before continuing with this section, if you wish for *more control* over your calculation than the previous section but *less bloat* to code than what follows, I suggest you look at the `geodpy.basic` function, which automates a good portion of the calculation. However, this is entirely optionnal as this function is merely a wrapper for the later steps of the current section. If you want to do this approach, complete steps 1 and 2, and intialize the dictionnary in step 4, then feed the variables you have made along the way to the `basic` function. See `basic.py` for the arguments you need to input.

#### 1. Establish your coordinate system
If you venture in `geodpy/coordinates.py`, you will see that some coordinate systems have already been defined for easy use. If you wish to have more specific coordinates system, you will need to create your own class that implements the `Coordinates` abstract class located in the same file. I suggest you copy/paste an already implemented class and modify it to your needs. Note that the `to_cartesian` method is optionnal if you do not intend to plot your data using the project's plotting tools.

Once that is done, you will need to unpack your `Coordinates.coords` attribute into 4 seperate variables (these are your individual coordinates). You will need them for the following step.


#### 2. Create the metric
Create a symbolic `sympy` **Matrix** object for your space-time metric. The metric needs to make use of the coordinates (sympy **Function** objects) defined in the previous step. You most not parametrized the metric by any other sympy **Functions**. Your metric should only contain your coordinates and constants.

#### 3. Compute the symbolic geodesics 
For this step, import `Geodesics` from `geodpy`. Create a `Geodesic` object by feeding the constructor your coordinate class and the metric. Upon creation, the object will automatically start computing.

#### 4. Compute the trajectory of a body
For this step, import `Body` from `geodpy`. Create a `Body` object by feeding the constructor your Geodesic object, as well as the initial position vector (python list of lenght 4) and the initial velocity vector (python list also of lenght 4). Notice that coordinate time `t` is considered a position, as in a position in space-time and not just space.

Afterwards, execute:
```python
body.solve_trajectory(**solver_kwargs)
```
This method is basically a wrapper for the scipy `solve_ivp` function. As such, the *parameters* you need to feed `solve_trajectory` are the same as the `solve_ivp` keyword arguments. Below is a dictionnary of all the parameters to feed the method:
```python
solver_kwargs = {
    "time_interval": (0,T),           
    "method"       : "Radau",          
    "max_step"     : T*1e-3,
    "atol"         : 1e-8,              
    "rtol"         : 1e-8,              
    "events"       : None,              
}
```
You can simpy unpack this as function parameters. Upon running, the code will solve the differential equation system established by the `Geodesics` object.

You can also calculate the norm of the velocity vector for each point using the `calculate_velocities` method of the `Body` object. The results will be store in the `body.vel_norm` class attribute.

#### 5. Plot your data
The results are stored in the `body.pos` and `body.vel` class attributes. However, the raw results, directly given by `solve_ivp` are stored in the `body.solver_result` class attribute, should you need them. As you may have guessed, `body.pos` and `body.vel` are respectively the position and velocity vectors of your body following the geodesic. To get the proper time (also known as the "interval") for each point, call `body.s`.

This project can also plot your data automatically and according to your coordinate system. To do this, import one of the non-abstract plotter classes located in `geodpy/plotter.py` and instantiate it. The object will offer the following methods originating the abstract class `BodyPlotter`:
```python
plot(title: str)
save_plot(file_name: str)

animate(frame_interval: list)
save_animation(file_name: str)

plot_velocity(title: str)
save_velocity(file_name: str)

show() # Shows all plots created up to now
```
In case you are working in a coordinate system that is NOT spherical or cartesian, then it is unsupported by geodpy for plotting. However, if you have correctly defined your Coordinate class from earlier, you may be able to convert your final results to cartesian or spherical coordinates. To do this, simply run:
```
cartesian_body = body.get_cartesian_body(**kwargs)
spherical_body = body.get_spherical_body(**kwargs)
```
which will create another body object with the correct position and velocity vectors in cartesian or spherical coordinates. The kwargs are the arguments of the `get_cartesian` or `get_spherical` methods from the Coordinates object. Indeed, transformation into another coordinate system may require additionnal parameters. You can then use `cartesian_body` or `spherical_body` to plot your data with your plotter object.

Depending on if you are using a 3D plotter or a 2D plotter, you have different methods available to add additionnal figures to the plot. For instance, you could add a black circle, representing a blackhole, if you wish. More info on these methods are provided in geodpy/README.md.

## Interface
If you wish to see a more detailed overview of all the classes and functions at your disposition, be sure to checkout the `README.md` located in the `geodpy` source code folder.


