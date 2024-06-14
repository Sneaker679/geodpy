# darkMatter
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
In the `examples` folder are some examples with many metrics, including the Schwarzschild, Kerr and Schwarzschild de Sitter metric. To simplify this break down of the code, I shall refer these metrics simply as `metric`. Inside the `metric` fodlers are many different configurations for testing purposes. The script `metric.py` is responsible for actually running the code given certain parameters. The other `auxiliary.py` files are specific configurations that call the functionalities `metric.py`. If you open these auxiliary files, you will will see a very short script with some parameters that you can modify to produce different geodesic results.

To run the configuration, simply run the script : `python3 auxiliary.py`. More details on the actual meaning of the parameters are given in the `README.md` of each `metric` example folders.

## Advanced Usage
Seeing as you have added the project folder to your python path, you can call the classes and functions of this code from any location in your computer. Once you have established a workspace, create an empty scrip and start coding!

The basic strategy to yield results is described below.

#### 0. Hold on!
Before continuing with this section, if you wish for *more control* over your calculation than the previous section but *less bloat* to code than what follows, I suggest you look at the `geodpy.basic` function, which automates a good portion of the calculation. However, this is entirely optionnal as this function is merely a wrapper for the later steps of the following procedure. If you want to do this approach, complete steps 1 and 2, and intialize the dictionnary in step 4, then feed the variables you have made along the way to the `basic` function. See `basic.py` for the arguments you need to input.

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
You can simpy unpack this in as function parameters. Upon running, the code will solve the differential equation system established by the `Geodesics` object.

You can also calculate the norm of the velocity vector for each point using the `calculate_velocities` method of the `Body` object. The results will be store in the `body.vel_norm` class attribute.

#### 5. Plot your data
The results are stored in the `body.pos` and `body.vel` class attributes. However, the raw results, directly given by `solve_ivp` are stored in the `body.solver_result` class attribute, should you need them. As you may have guessed, `body.pos` and `body.vel` are respectively the position and velocity vectors of your body following the geodesic. To get the proper time (also known as the "interval") for each point, call `body.s`.

This project can also plot your data automatically and according to your coordinate system. To do this, import `BodyPlotter` from `geodpy`. Create a `BodyPlotter` object by feeding the constructor your `Body` object. The class offers the following methods:
```python
plot(title: str)
save_plot(file_name: str)

animate(frame_interval: list)
save_animation(file_name: str)

plot_velocity(title: str)
save_velocity(file_name: str)

set_patches(patches: list[matplotlib.patches]) # Add matplotlib patches to your graphs
show() # Shows all plots created up to now
```
If you get a `NotImplementedError`, it may be because your coordinate system is not yet implemented or is not supported. This is where your Coordinate class `to_cartesian` comes into play. You won't need to call it directly however. In your script, run:
```
cartesian_body = body.get_cartesian_body(**kwargs)
```
which will create another body object with the correct position and velocity vectors in cartesian coordinates. The kwargs comes from your `get_cartesian` method, which may need additionnal parameters depending on your coordinate system. You can then use `cartesian_body` to plot your data with the `BodyPlotter` object.


