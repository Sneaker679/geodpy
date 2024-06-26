PARAMETERS DEFINITION:
- ro -> initial distance from origin;
- rs -> schwarzschild radius of the body curving space-time, also equal to twice the mass;
- Λ  -> the cosmological constant, equal to 1.11e-52 m^-2 by default;
- h  -> initial angular momentum;
- k  -> initial energy or, more specifically, (total energy)/(mc^2).

To run a calculation, use the python command on any of the files except `sitter_schwarzschild.py`. For example:
```bash
python3 strong_expansion.py
```
will produce plots showing a geodesic in a situation where the expansion of the universe is very strong - so strong that it escapes its almost circular orbit.
