## Description
The Schwarzschild metric describes a non-rotating blackhole.
 
PARAMETERS DEFINITION:
- ro -> initial distance from origin;
- rs -> schwarzschild radius of the body curving space-time, also equal to twice the mass;
- h  -> initial angular momentum;
- k  -> initial energy or, more specifically, (total energy)/(mc^2).

## Running examples
To run a calculation, use the python command on any of the files except `schwarzschild.py`. For example:
```bash
python3 1_clover_traj.py
```
will produce plots showing a body falling into a Schwarzschild blackhole. By default, the examples produce almost no outputs in the command line. For more explicit outputs, edit the example scripts and change the `verbose` parameter to `2`. You can also edit many more parameters by modifying the scripts, like the file names for the outputs or the physical parameters of the simulation as described above.

This folder contains 3 examples:
- `1_clover_traj.py` : A body orbitting a Schwarzschild blackhole in a clover like shape. This is possible because of the intense precession of the orbit after each rotation.
- `2_crashing_traj.py` : A body falling into a Schwarzschild blackhole. Because of a singularity in the metric at r=rs, the simulation stops upon reaching the event horizon. 
- `3_earth_ellipse.py` : The Earth orbitting the sun for one year, using the actual angular momentum and energy of our planet on this orbit for the calculation. This produces an elliptical orbit, as expected.

