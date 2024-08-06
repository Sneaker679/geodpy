## Description
The Kerr metric describes a rotating blackhole. When blackholes spin, they drag the space-time around them, thus aligning the geodesics around the equator.

PARAMETERS DEFINITION:
- ro -> initial distance from origin;
- rs -> schwarzschild radius of the body curving space-time, also equal to twice the mass;
- a  -> rotating speed of the blackhole and its absolute value must be smaller than half of rs;
- σ  -> direction of the orbit : 1 means co-rotation and -1 means counter-rotation;
- h  -> initial angular momentum;
- k  -> initial energy or, more specifically, (total energy)/(mc^2).

PLOT LEGEND
- Blue circle -> Inner horizon;
- Black circle -> Outer horizon, the surface of the blackhole;
- Red circle -> Ergosphere region, where nothing can NOT move.

## Running examples
To run a calculation, use the python command on any of the files except `kerr.py`. For example:
```bash
python3 1_crashing_traj_2D.py
```
will produce plots showing the geodesic of a body plunging in a rotating blackhole. By default, the examples produce almost no outputs in the command line. For more explicit outputs, edit the example scripts and change the `verbose` parameter to `2`. You can also edit many more parameters by modifying the scripts, like the file names for the outputs or the physical parameters of the simulation as described above.

This folder contains 4 examples:
- `1_crashing_traj_2D.py` : A body plunges into a rotating blackhole. As it approaches, its trajectory abruptly changes direction and starts making circles in the same direction as the rotation of the blackhole.
- `2_crashing_traj_3D.py` : A body plunges into a rotating blackhole. As it approaches, its trajectory abruptly changes direction and also aligns itself with the equator of the blackhole.
- `3_crashing_top_3D.py` : A body is dropped near the axis of rotation of the blackhole. When close to the event horizon, the body very rapidly realigns itself with the equator until it stabilizes.
- `4_orbit_traj_2D.py` : A body is orbitting the rotating blackhole in a near circular orbit.
- `5_orbit_traj_3D.py` : A body is orbitting the rotating blackhole while oscillating around the equatorial plane.
