from geodesics import Geodesics
from integration import integrate_diff_eqs, DiffEquationsSolution

from utilities.coord_transformation import spherical_to_cartesian
from utilities.velocities import calculate_velocities

from sympy import *
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = True
orbit_pdf_name = "outputs/o_.pdf"
orbit_mp4_name = "outputs/o_.mp4"
velocity_pdf_name = "outputs/v_.pdf"
plot_velocity = False
plot_orbit = True


# Interval config
s = symbols('s')

# Initial values
initial_values = [0, 0, 0, 0, 0, 0, 0, 0]

# Integration config
time_interval = (0,1000)
max_time_step = 0.01

# Metric config
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
coordinates : list[Function] = [t, r, θ, φ]

gₘₖ = Matrix([
    [0          ,0          ,0          ,0          ],
    [0          ,0          ,0          ,0          ],
    [0          ,0          ,0          ,0          ],
    [0          ,0          ,0          ,0          ]
])

# Integration config
T = 1000
time_interval = (0,T)
max_time_step = 1


if __name__ == "__main__":

    # Calculating geodesics
    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics._dₛuᵏ
    geodesics_lambda = geodesics._dₛuᵏ_lambda

    # Integration of ODE system
    print("Integrating")
    result: DiffEquationsSolution = integrate_diff_eqs(geodesics = geodesics, time_interval = time_interval, initial_values = initial_values, max_step = max_time_step)

    # Velocity calculation
    speed_equation : Function = (r.diff(s)**2 + r**2 * φ.diff(s))**(1/2)
    velocities = calculate_velocities(speed_equation, result)

    # Printing
    if print_output is True:
        print("Geodesic differential equations: ")
        for equation in geodesics_symbolic:
            pprint(equation)
            print()

        print("Integration result: ")
        print(result.solver_result)


    # Plotting
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    if plot_velocity is True:
        # Plotting velocity(t)
        fig, ax = plt.subplots()
        plt.title("Velocity of a star orbiting a blackhole")
        ax.set_ylabel("Velocity")
        ax.set_xlabel("Time")
        plt.plot(result.x0,velocities)
        fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    if plot_orbit is True:
        # Plotting orbit
        fig, ax = plt.subplots()

        ...

        fig.savefig(orbit_pdf_name)
        plt.show()
