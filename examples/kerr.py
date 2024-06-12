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

orbit_pdf_name = "outputs/o_kerr.pdf"
orbit_mp4_name = "outputs/o_kerr.mp4"
velocity_pdf_name = "outputs/v_kerr.pdf"

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
def circ(r: float, rs: float, a: float, σ: int) -> tuple[float,float]:
    assert a <= rs/2 
    rot_term = σ*a*np.sqrt(rs/(2*r*r*r))
    num_k = 1 - rs/r + rot_term
    num_h = 1 + a*a/(r*r) - 2*rot_term
    den = np.sqrt( 1 - 1.5*rs/r + 2*rot_term )
    return num_k/den, σ*np.sqrt(r*rs/2)*num_h/den # k, h
    
def radii(rs: float, a: float) -> tuple[float,float]:
    assert a <= rs/2 
    return 1/2 * (rs + np.sqrt(rs*rs - 4*a*a)), 1/2 * (rs - np.sqrt(rs*rs - 4*a*a))

def contravariant_tdot(r: float, rs: float, a: float, k: float, h: float) -> float:
    Δ = r*r + a*a - r*rs
    return 1/Δ * ((r*r + a*a + a*a*rs/r)*k - a*rs*h/r)

def contravariant_rdot2(r: float, rs: float, a: float, k: float, h: float) -> float:
    rdot2 = k*k - 1 + rs/r + (a*a*(k*k - 1) - h*h)/(r*r) + rs*(h - a*k)*(h - a*k)/(r*r*r)
    if rdot2 < 0:
        return 0
    else:
        return k*k - 1 + rs/r + (a*a*(k*k - 1) - h*h)/(r*r) + rs*(h - a*k)*(h - a*k)/(r*r*r)

def contravariant_phidot(r: float, rs: float, a: float, k: float, h: float) -> float:
        return 1/(r*r + a*a - r*rs) * (a*rs*k/r + (1 - rs/r)*h)

a = 0.4
rs = 1
r_ext, r_int = radii(rs, a) 
ro = 5
σ = -1 # 1 or -1
k, h = circ(ro, rs, a, σ)
h -= 0.3
dₛt = contravariant_tdot(ro, rs, a, k, h)
dₛr = contravariant_rdot2(ro, rs, a, k, h)
dₛφ = contravariant_phidot(ro, rs, a, k, h)
initial_values = [0, ro, np.pi/4, 0, dₛt, dₛr, 0, dₛφ] #0.00185

# Metric config
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
p2 = r*r + a*a*(cos(θ))**2 
Δ = r*r + a*a - r*rs
coordinates : list[Function] = [t, r, θ, φ]

gₘₖ = Matrix([
    [1-rs*r/(p2)             ,0      ,0    ,(a*r*rs*sin(θ)**2)/(p2)                           ],
    [0                       ,-p2/Δ  ,0    ,0                                                 ],
    [0                       ,0      ,-p2  ,0                                                 ],
    [(a*r*rs*sin(θ)**2)/(p2) ,0      ,0    ,-(r*r + a*a + (a*a*r*rs*sin(θ)**2)/(p2))*sin(θ)**2]
])

# Integration config
T = 1000
time_interval = (0,T)
max_time_step = 0.1


if __name__ == "__main__":
    print(f"a={a}, k={k}, h={h}, r_ext={r_ext}, r_int={r_int}, ro={ro}, dₛr={dₛr}")

    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics._dₛuᵏ
    geodesics_lambda = geodesics._dₛuᵏ_lambda
    import inspect
    for func in geodesics_lambda:
        print(inspect.getsourcelines(func), end="\n\n\n\n")

    # Integration of ODE system
    print("Integrating")
    result: DiffEquationsSolution = integrate_diff_eqs(geodesics = geodesics, time_interval = time_interval, initial_values = initial_values, max_step = max_time_step, atol=1e-10, rtol= 1e-10)

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
        if v_save_pdf is True: fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    max_radial_distance = np.max(result.x1)
    if plot_orbit is True:
        # Plotting orbit
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        plt.title("Orbit of a star around a blackhole")
        ax.add_patch(patches.Circle((0,0), r_ext, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.add_patch(patches.Circle((0,0), r_int, transform=ax.transData._b, edgecolor="b")) # blackhole
        ax.plot(result.x3, np.sqrt(result.x1*result.x1 + a*a))

        ax.set_ylim(0, max_radial_distance*6/5)

        if save_pdf is True: fig.savefig(orbit_pdf_name)
        plt.show()

    if animate is True:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.add_patch(patches.Circle((0,0), r_ext, transform=ax.transData._b, edgecolor="k", fill=True, facecolor='k')) # blackhole
        ax.add_patch(patches.Circle((0,0), r_int, transform=ax.transData._b, edgecolor="b")) # blackhole
        line = ax.plot(result.x3, np.sqrt(result.x1*result.x1 + a*a))[0]
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

        ani = animation.FuncAnimation(fig=fig, func=update, save_count=result.x1.shape[0], interval = 20)
        plt.show()
        if save_mp4 is True: ani.save(orbit_mp4_name)
