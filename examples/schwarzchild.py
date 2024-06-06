from geodesics import Geodesics
from integration import integrate_diff_eqs, DiffEquationsSolution

from utilities.coord_transformation import spherical_to_cartesian
from utilities.velocities import calculate_velocities

from sympy import *
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = True
orbit_pdf_name = "outputs/o_schwarzschild.pdf"
orbit_mp4_name = "outputs/o_schwarzschild.mp4"
velocity_pdf_name = "outputs/v_schwarzschild.pdf"
plot_velocity = False
plot_orbit = False
animate = False

# Interval config
s = symbols('s')

# Initial values
rs = 1
ro = 5 * rs
k = 1 #(1-rs/ro)/np.sqrt(1-3*rs/(2*ro))
h = 0 #np.sqrt((rs/ro + (k*k - 1))*ro*ro/(1 - rs/ro)) - 0.5
initial_values = [0, ro, np.pi/2, 0, k/(1-rs/ro), 0, 0, h/(ro**2)]

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

# Integration config
T = 100
time_interval = (0,T)
max_time_step = 0.01


if __name__ == "__main__":
    print(f"k={k}\nh={h}")

    # Calculating geodesics
    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics._dₛuᵏ
    geodesics_lambda = geodesics._dₛuᵏ_lambda

    # Integration of ODE system
    print("Integrating")
    result: DiffEquationsSolution = integrate_diff_eqs(geodesics = geodesics, time_interval = time_interval, initial_values = initial_values, max_step = max_time_step, events=event)

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

        from validationTests.schwarzschild import *
        print(f"Energy conserved: {check_k(result.x1, result.dx1, rs=rs)}")
        print(f"Angular momentum conserved: {check_h(result.x1, result.dx3, rs=rs)}")


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
        #fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    max_radial_distance = np.max(result.x1)
    if plot_orbit is True:
        # Plotting orbit
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        plt.title("Orbit of a star around a blackhole")
        ax.add_patch(patches.Circle((0,0), rs, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.plot(result.x3, result.x1)

        ax.set_ylim(0, max_radial_distance*6/5)

        #fig.savefig(orbit_pdf_name)
        plt.show()

    if animate is True:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.add_patch(patches.Circle((0,0), rs, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        line = ax.plot(result.x3, result.x1)[0]
        ax.set_ylim(0, max_radial_distance*6/5)

        def update(frame):
            try:
                plt.title(f"r = {result.x1[frame]}, t = {int(result.x0[frame])}, s = {int(result.s[frame])}")
            except:
                pass
            r = result.x1[:frame]
            phi = result.x3[:frame]
            # update the line plot:
            line.set_xdata(phi)
            line.set_ydata(r)
            return line

        ani = animation.FuncAnimation(fig=fig, func=update, save_count=result.x0.shape[0], interval = 20)
        #ani.save(orbit_mp4_name)
        plt.show()
    print(result.x0[-1])
    print(result.s[-1])
    print(result.dx0[-1])
