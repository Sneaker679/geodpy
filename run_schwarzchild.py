from sympy import *
from geodesics import *

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = True
orbit_pdf_name = "outputs/o_schwarzschild.pdf"
velocity_pdf_name = "outputs/v_schwarzschild.pdf"
plot_velocity = False
plot_orbit = True

# Initial values
import numpy as np
rs = 1
ro = 4 * rs
k = (1-rs/ro)/np.sqrt(1-3*rs/(2*ro)) # circular orbit
h = np.sqrt((rs/ro + (k*k - 1))*ro*ro/(1 - rs/ro)) # circular orbit
initial_values = [0, ro, pi/2, 0, k/(1-rs/ro), 0, 0, h/(ro**2)]

# Integration config
time_interval = (0,1000)
max_time_step = 0.1

# Interval config
s = symbols('s')

# Metric config
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
coordinates : list[Function] = [t, r, θ, φ]

gₘₖ = Matrix([
    [1-rs/r     ,0          ,0          ,0          ],
    [0          ,1/(rs/r-1) ,0          ,0          ],
    [0          ,0          ,-r**2      ,0          ],
    [0          ,0          ,0          ,-r**2 * sin(θ)**2]
])


if __name__ == "__main__":

    # Calculating geodesics
    geodesics_obj : list = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics_obj._dₛuᵏ
    geodesics_lambda = geodesics_obj._dₛuᵏ_lambda

    # Integration of ODE system
    ode_result = geodesics_obj.integrate(initial_values = initial_values, time_interval = time_interval, max_time_step = max_time_step)

    # Velocity calculation
    speed_equation : Function = (r.diff(s)**2 + r**2 * φ.diff(s))**(1/2)
    velocities = geodesics_obj.calculate_velocities(speed_equation)

    # Printing
    if print_output is True:
        print("Geodesic differential equations: ")
        for equation in geodesics_symbolic:
            pprint(equation)
            print()

        print("Integration result: ")
        print(ode_result)

        from validationTests.val_schwarzschild import *
        print(f"Energy conserved: {check_k(ode_result.y[1], ode_result.y[4], rs=rs)}")
        print(f"Angular momentum conserved: {check_h(ode_result.y[1], ode_result.y[7], rs=rs)}")


    # Plotting
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    if plot_velocity is True:
        # Plotting velocity(t)
        fig, ax = plt.subplots()
        plt.title("Velocity of a star orbiting a blackhole")
        ax.set_ylabel("Velocity")
        ax.set_xlabel("Time")
        plt.plot(ode_result.y[0],velocities)
        fig.savefig(velocities_pdf_name)
        plt.show()
        plt.close()

    if plot_orbit is True:
        # Plotting orbit
        # Getting 
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        
        plt.title("Orbit of a star around a blackhole")
        ax.add_patch(patches.Circle((0,0), 1, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.plot(ode_result.y[3],ode_result.y[1])

        max_radial_distance = np.max(ode_result.y[1])
        ax.set_ylim(0,max_radial_distance*6/5)

        fig.savefig(orbit_pdf_name)
        plt.show()
