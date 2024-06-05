from sympy import *
from geodesics import *
from coord_transformation import spherical_to_cartesian
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = True
orbit_pdf_name = "outputs/o_kerr.pdf"
velocity_pdf_name = "outputs/v_kerr.pdf"
plot_velocity = False
plot_orbit = True
animate = True

# Interval config
s = symbols('s')

# Initial values
a = 0.4
rs = 1
ro = 5 * rs
initial_values = [0, ro, np.pi/2, 0, 1, 0, 0, -0.02]

# Metric config
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
p = r*r + a*a*cos(θ)**2 
Δ = r*r + a*a - r*rs
coordinates : list[Function] = [t, r, θ, φ]

gₘₖ = Matrix([
    [1-rs*r/(p*p)             ,0      ,0    ,(a*r*rs*sin(θ)**2)/(p*p)                            ],
    [0                        ,-p*p/Δ ,0    ,0                                                   ],
    [0                        ,0      ,-p*p ,0                                                   ],
    [(a*r*rs*sin(θ)**2)/(p*p) ,0      ,0    ,-(r*r + a*a + (a*a*r*rs*sin(θ)**2)/(p*p))*sin(θ)**2]
])

# Integration config
time_interval = (0,10000)
max_time_step = 1


if __name__ == "__main__":
    print(f"a={a}")

    # Calculating geodesics
    print("Calculating geodesics")
    geodesics_obj : list = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics_obj._dₛuᵏ
    geodesics_lambda = geodesics_obj._dₛuᵏ_lambda

    # Integration of ODE system
    print("Integrating")
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
        fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    max_radial_distance = np.max(ode_result.y[1])
    external_radius, internal_radius = 1/2 * (rs + np.sqrt(rs*rs - 4*a*a)), 1/2 * (rs - np.sqrt(rs*rs - 4*a*a))
    if plot_orbit is True:
        # Plotting orbit
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        plt.title("Orbit of a star around a blackhole")
        ax.add_patch(patches.Circle((0,0), external_radius, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.add_patch(patches.Circle((0,0), internal_radius, transform=ax.transData._b, edgecolor="b")) # blackhole
        ax.plot(ode_result.y[3], ode_result.y[1])

        ax.set_ylim(0, max_radial_distance*6/5)

        fig.savefig(orbit_pdf_name)
        plt.show()

    if animate is True:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.add_patch(patches.Circle((0,0), external_radius, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.add_patch(patches.Circle((0,0), internal_radius, transform=ax.transData._b, edgecolor="b")) # blackhole
        line = ax.plot(ode_result.y[3], ode_result.y[1])[0]
        ax.set_ylim(0, max_radial_distance*6/5)

        def update(frame):
            try:
                plt.title(f"r = {ode_result.y[1][frame]}, t = {int(ode_result.y[0][frame])}, s = {int(ode_result.t[frame])}")
            except:
                pass
            r = ode_result.y[1][:frame]
            phi = ode_result.y[3][:frame]
            # update the line plot:
            line.set_xdata(phi)
            line.set_ydata(r)
            return line

        ani = animation.FuncAnimation(fig=fig, func=update, save_count=ode_result.y.shape[1], interval = 20)
        plt.show()
