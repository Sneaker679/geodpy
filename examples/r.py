from geodesics import Geodesics
from body import Body

from utilities.coord_transformation import spherical_to_cartesian
from utilities.velocities import calculate_velocities
from utilities.bodyplotter import BodyPlotter

from sympy import *
import matplotlib.animation as animation
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

orbit_pdf_name = "outputs/o_schwarzschild.pdf"
orbit_mp4_name = "outputs/o_schwarzschild.mp4"
velocity_pdf_name = "outputs/v_schwarzschild.pdf"
s = symbols('s')

rs = 3.117165937356868 #a.l
ro = 5e14 #5e5 a.l
k = (1-rs/ro)/np.sqrt(1-3*rs/(2*ro))
h = np.sqrt((rs/ro + (k*k - 1))*ro*ro/(1 - rs/ro))
initial_values = [0, ro, np.pi/2, 0, k/(1-rs/ro), 0, 0, h/(ro**2)]

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

T = ro*1e10
time_interval = (0,T)
max_time_step = T*1e-3


if __name__ == "__main__":
    print(f"k={k}\nh={h}")
    print("Calculating geodesics")
    geodesics: Geodesics = Geodesics(s, gₘₖ, coordinates)
    body = Body(geodesics, initial_values[0:4], initial_values[4:8])
    print("Solving trajectory")
    body.solve_trajectory(time_interval = time_interval, max_step = max_time_step, rtol=1e-10, atol=1e-10)
    speed_equation : Function = (r.diff(s)**2 + r**2 * φ.diff(s))**(1/2)
    velocities = calculate_velocities(speed_equation, body)

    #import inspect
    #print(inspect.getsourcelines(geodesics._dₛuᵏ_lambda[1]))

    # Printing
    print("Geodesic differential equations: ")
    for equation in geodesics._dₛuᵏ:
        pprint(equation)
        print()

    print("Integration result: ")
    print(body.solver_result)

    from validationTests.schwarzschild import *
    print(f"Energy conserved: {check_k(body.pos[1], body.vel[1], rs=rs)}")
    print(f"Angular momentum conserved: {check_h(body.pos[1], body.vel[3], rs=rs)}")


    # Plotting

    plotter = BodyPlotter(body)
    plotter.set_polar()
    plotter.plot("Cool title")
    plotter.animate()
    plotter.show()
