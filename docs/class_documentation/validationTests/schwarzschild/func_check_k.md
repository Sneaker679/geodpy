# def check\_k()
DESCRIPTION: Verifies if the energy of a solved trajectory in the Schwarzschild metric is conserved.

RETURNS - None, but prints to the screen if the energy was conserved.

PARAMETERS
- body: `geodpy.Body` ~~ Body to analyse. The trajectory needs to be already solved or there is no point in using this function.
- rs: `int` ~~ Schwarzschild radius used for the simulation.
