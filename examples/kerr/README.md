PARAMETERS DEFINITION:
- ro -> initial distance from origin;
- rs -> schwarzschild radius of the body curving space-time, also equal to twice the mass;
- a  -> rotating speed of the blackhole and its absolute value must be smaller than half of rs;
- σ  -> direction of the orbit : 1 means co-rotation and -1 means counter-rotation;
- h  -> initial angular momentum;
- k  -> initial energy or, more specifically, (total energy)/(mc^2).

To run a calculation, use the python command on any of the files except `kerr.py`. For example:
```bash
python3 sucked_in_2D.py
```
will produce plots showing the geodesic of a body plunging in a rotating blackhole.
