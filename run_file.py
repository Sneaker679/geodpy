from sympy import *
from geodesics import *

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

# ===== PARAMETERS =====

print_output = True
orbit_pdf_name = "outputs/o_.pdf"
velocity_pdf_name = "outputs/v_.pdf"
plot_velocity = False
plot_orbit = True

# Initial values
initial_values = [0, 0, 0, 0, 0, 0, 0, 0]

# Integration config
time_interval = (0,1000)
max_time_step = 0.01

# Interval config
s = symbols('s')

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


if __name__ == "__main__":

    # Calculating geodesics
    geodesics_obj : list = Geodesics(s, gₘₖ, coordinates)
    geodesics_symbolic = geodesics_obj._dₛuᵏ
    geodesics_lambda = geodesics_obj._dₛuᵏ_lambda

    # Integration of ODE system
    ode_result = geodesics_obj.integrate(initial_values = initial_values, time_interval = time_interval, max_time_step = max_time_step)

    # Velocity calculation
    speed_equation : Function = None
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
        fig.savefig(velocity_pdf_name)
        plt.show()
        plt.close()

    if plot_orbit is True:
        # Plotting orbit
        # Getting 
        fig, ax = plt.subplots()

        ...

        fig.savefig(orbit_pdf_name)
        plt.show()
