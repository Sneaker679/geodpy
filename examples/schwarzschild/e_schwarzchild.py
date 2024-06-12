from geodesics import Geodesics
from body import Body

from utilities.coord_transformation import spherical_to_cartesian
from utilities.velocities import calculate_velocities
from utilities.bodyplotter import BodyPlotter

from sympy import *
import matplotlib.animation as animation
import numpy as np

def kcirc(rs, r) -> float:
    return (1-rs/r)/np.sqrt(1-3*rs/(2*r))

def hcirc(rs, r) -> float:
    k = kcirc(rs, r)
    return np.sqrt((rs/r + (k*k - 1))*r*r/np.exp(rs/r))

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

save_pdf = True 
save_mp4 = False # Takes time
v_save_pdf = False

# Animation parameters
frame_interval = 1

# Interval config
s = symbols('s')

# Initial values
rs = 3.14
ro = 5e15

k, h = kcirc(rs,ro), hcirc(rs,ro)
#h += 2e7
pos = [0, ro, np.pi/2, 0]
vel = [k/(1-rs/ro), 0, 0, h/(ro**2)]
print(vel[-1], " = ", np.sqrt(np.exp(-rs/ro)*rs/(2*ro*ro*ro)))

# Metric config
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
coordinates : list[Function] = [t, r, θ, φ]

gₘₖ = Matrix([
    [exp(-rs/r) ,0          ,0          ,0          ],
    [0          ,-exp(rs/r) ,0          ,0          ],
    [0          ,0          ,-r**2      ,0          ],
    [0          ,0          ,0          ,-r**2 * sin(θ)**2]
])

# Integration config
T = ro*1.3e8
time_interval = (0,T)
max_time_step = T*1e-3



if __name__ == "__main__":
    print(f"k={k}\nh={h}")

    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    geodesics_sym = geodesics._dₛuᵏ
    for ele in geodesics_sym:
        pprint(ele)
    body = Body(geodesics, pos, vel)

    print("Solving trajectory")
    body.solve_trajectory(time_interval = time_interval, max_step = max_time_step, rtol=1e-10, atol=1e-10)

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
    import matplotlib.patches as patches
    ps = [patches.Circle((0,0), rs, edgecolor="k", fill=True, facecolor='k')] # blackhole
    plotter = BodyPlotter(body)
    plotter.set_polar()
    plotter.set_patches(ps)
    plotter.plot(title="Trajectory of a star orbiting a blackhole")
    plotter.animate()
    plotter.show()

    # Velocity
    speed_equation : Function = (r.diff(s)**2 + r**2 * φ.diff(s))**(1/2)
    velocities = calculate_velocities(speed_equation, body)
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

