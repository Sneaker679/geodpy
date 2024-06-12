from geodesics import Geodesics
from integration import integrate_diff_eqs, DiffEquationsSolution
from body import Body

from utilities.coord_transformation import spherical_to_cartesian
from utilities.velocities import calculate_velocities

from sympy import *
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = False

orbit_pdf_name = "outputs/o_schwarzschild.pdf"
orbit_mp4_name = "outputs/o_schwarzschild.mp4"
velocity_pdf_name = "outputs/v_schwarzschild.pdf"

plot_orbit = True
animate = True
plot_velocity = False

save_pdf = True # Takes time
save_mp4 = False
v_save_pdf = False

# Animation parameters
frame_interval = 1

# Interval config
s = symbols('s')

# Initial values
rs = 3.117165937356868 #a.l
ro = 5e14 #5e5 a.l
k = (1-rs/ro)/np.sqrt(1-3*rs/(2*ro))
h = np.sqrt((rs/ro + (k*k - 1))*ro*ro/(1 - rs/ro))
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
T = ro*1e11
time_interval = (0,T)
max_time_step = T*1e-4


if __name__ == "__main__":
    print(f"k={k}\nh={h}")

    # Calculating geodesics
    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    #import inspect
    #print(inspect.getsourcelines(geodesics._dₛuᵏ_lambda[1]))

    # Integration of ODE system
    print("Solving trajectory")
    body = Body(geodesics, initial_values[0:4], initial_values[4:8])
    body.solve_trajectory(time_interval = time_interval, max_step = max_time_step, rtol=1e-10, atol=1e-10)

    # Velocity calculation
    speed_equation : Function = (r.diff(s)**2 + r**2 * φ.diff(s))**(1/2)
    velocities = calculate_velocities(speed_equation, body)

    # Printing
    if print_output is True:
        print("Geodesic differential equations: ")
        for equation in geodesics_symbolic:
            pprint(equation)
            print()

        print("Integration result: ")
        print(body.solver_result)

        from validationTests.schwarzschild import *
        print(f"Energy conserved: {check_k(body.pos[1], body.vel[1], rs=rs)}")
        print(f"Angular momentum conserved: {check_h(body.pos[1], body.vel[3], rs=rs)}")


    # Plotting
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    if plot_velocity is True:
        # Plotting velocity(t)
        fig, ax = plt.subplots()
        plt.title("Velocity of a star orbiting a blackhole")
        ax.set_ylabel("Velocity")
        ax.set_xlabel("Time")
        plt.plot(body.pos[0], velocities)
        if v_save_pdf is True: fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    max_radial_distance = np.max(body.pos[1])
    if plot_orbit is True:
        # Plotting orbit
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        plt.title("Orbit of a star around a blackhole")
        ax.add_patch(patches.Circle((0,0), rs, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.plot(body.pos[3], body.pos[1])

        ax.set_ylim(0, max_radial_distance*6/5)

        if save_pdf is True: fig.savefig(orbit_pdf_name)
        plt.show()

    if animate is True:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.add_patch(patches.Circle((0,0), rs, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        line = ax.plot(body.pos[3], body.pos[1])[0]
        ax.set_ylim(0, max_radial_distance*6/5)

        def update(frame):
            try:
                plt.title(f"r = {body.pos[1][frame]}, t = {int(body.pos[0][frame])}, s = {int(body.s[frame])}")
            except:
                pass
            r = body.pos[1][:frame]
            phi = body.pos[3][:frame]
            # update the line plot:
            line.set_xdata(phi)
            line.set_ydata(r)
            return line

        ani = animation.FuncAnimation(fig=fig, func=update, save_count=body.pos[0].shape[0], interval = 20)
        plt.show()
        if save_mp4 is True: ani.save(orbit_mp4_name)
