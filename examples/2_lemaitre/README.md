## Description
The Lemaitre metric represents a Schwarzschild blackhole, but using a free-falling coordinate system. This prevent the appearance of a singularity at r=rs.

PARAMETERS DEFINITION:
- ro -> initial distance from origin;
- rs -> schwarzschild radius of the body curving space-time, also equal to twice the mass;
- h  -> initial angular momentum;
- k  -> initial energy or, more specifically, (total energy)/(mc^2).

## Running examples
To run a calculation, use the python command on any of the files except `lemaitre.py`. For example:
```bash
python3 1_crashing_trajectory.py
```
will produce a plot showing a body falling into a Schwarzschild blackhole. By default, the examples produce almost no outputs in the command line. For more explicit outputs, edit the example scripts and change the `verbose` parameter to `2`. You can also edit many more parameters by modifying the scripts, like the file names for the outputs or the physical parameters of the simulation as described above.

This folder contains 1 example:
- `1_crashing_trajectory.py` : Shows a body falling into a Schwarzschild blackhole, similarly to the Schwarzschild example of this library. Since we are using lemaitre coordinates, there is no more singularity in the calculation when r=rs. As such, we can observe the trajectory of the body while it is inside the blackhole, in contrast to the standard Schwarzschild metric where it would stop at the horizon.
