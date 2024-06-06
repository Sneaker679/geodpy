# darkMatter
Dark Matter is a scam and we'll prove it (at least we hope so).

The current version of this code is devoid of a number of features needed for the project. Currently, only geodesics differential equations may be calculated.

## Requirements
- matplotlib
- sympy
- scipy
- numpy

## Usage
Add the `source` folder to your directory by adding this line to your .basrc or .zshrc file:
```bash
export PYTHONPATH="${PYTHONPATH}:/home/codemaster/dev/projects/darkMatter/source"
```
or simply run it once directly in the terminal for single use cases.

In the `examples` folder are 2 examples, one with the Schwarzschild metric and another with the Kerr metric. If you open them, you can modify the parameters to your liking and get different solutions. Note that for the initial conditions list you need to configure, the ordering of the elements is : [t, r, theta, phi, dot t, dot r, dot theta, dot phi].

The coordinates themselves need to be Sympy Function objects, and the interval s (which corresponds to the proper time) needs to be a Sympy Symbol object.

To run the project, simply run the file with the python interpreter.
