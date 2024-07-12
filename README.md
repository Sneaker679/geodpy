# geodpy
This code aims to simulate geodesics given an arbitrary space-time metric.

## Capabilities
- Calculate symbolic geodesics
- Solve the trajectory of a body given an arbitrary metric and symbolic geodesics.
- Calculate the norm of the velocity of a body.
- Plot the trajectories on matplotlib in both 2D and 3D.

## Requirements
- matplotlib
- sympy
- scipy
- numpy

You can install these dependencies using:
```bash
pip install matplotlib numpy scipy sympy
```

## Installation
Clone the repository and go to the main folder `geodpy_lib`. You can use these commands:
```bash
git clone https://github.com/Sneaker679/geodpy_lib
cd geodpy_lib
```

In order to be able to import the classes and functions of this library, you will need to add the `geodpy_lib` folder to your PYTHON PATH. If you are already located in this folder, you can run the following command.
```bash
export PYTHONPATH="$(pwd):$PYTHONPATH"
```
To add the folder permanently to your PYTHON PATH, run this command instead.
```bash
echo 'export PYTHONPATH="$HOME'${PWD/#$HOME/}':$PYTHONPATH"' >> $HOME/.bashrc
```
or, for zsh terminals, run this.
```bash
echo 'export PYTHONPATH="$HOME'${PWD/#$HOME/}':$PYTHONPATH"' >> $HOME/.zshrc
```

## Basic Usage -> Using the examples

### Example with the Schwarzschild metric
In the `geodpy_lib/examples/schwarzschild` folder, run any of the python files except for `schwarzschild.py` (since it acts as a module for the other files). For instance, you could run:
```bash
python3 near_horizon.py
```
which will run a configuration of the Schwarzschild metric where the body in orbit is very close to the event horizon of the Schwarzschild black hole. A plot should be displayed on the screen using `matplotlib`.

### Structure of the examples
With the last example in mind, here is a more detailed overlook of how the examples are structured. This section will make it easier to understand how you can customize the orbits to your liking and experiment with the code.

In the `examples` folder are many examples that simulate geodesics with varied metrics, including the Schwarzschild, Kerr and Schwarzschild de Sitter metric. All these folders work in the same way. Taking the schwarzschild folder as an example, inside it are many files, the main one being `schwarzschild.py`. This script acts as a python module for the other files. Inside this code, there is a `schwarzschild()` function, which you can call with varied parameters to generate different geodesics. The other files in the `schwarzschild` folder are simple sripts who call the `schwarzschild()` function with different initial values. As it was shown in the previous section, the `near_horizon.py` script, for example, yields a geodesic simulated near the event horizon of a non rotating Schwarzschild blackhole. You can run the other examples in the other folders the same way.

The README inside each example folders specifies the meaning of the constants and quantities used.

## Advanced Usage
For more advance usages, refer to `geodpy_lib/docs/HowTo_trajectories.md`, `geodpy_lib/docs/HowTo_coordinates.md` and `geodpy_lib/docs/HowTo_plotters.md`

## Interface
If you wish to see a more detailed overview of all the classes and functions at your disposition, be sure to checkout the `geodpy_lib/docs/class_documentation/`. There are many Markdown files there explaining how all the classes and functions work. The REAMDEs in this folder also specify how you can import them.
