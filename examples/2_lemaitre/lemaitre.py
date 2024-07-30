from geodpy import Geodesics, Body, basic
from geodpy.plotters import PolarPlot
from geodpy.coordinates import Lemaitre

from sympy import *
import numpy as np

import os

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# Returns h for a circular orbit
def hcirc(rs: float, r: float) -> float:
    po = 2/3 * np.sqrt(r*r*r/rs)
    return np.sqrt( 2/9 * (3/2)**(8/3) * rs**(4/3) * po**(2/3) * 1/(1 - 3/2 * (2/3 * rs/po)**(2/3)) )

# Schwarzschild example function
def lemaitre(rs: float, ro: float, h: float, sim_T: float|None = None, output_kwargs: dict = {}, verbose: int = 1) -> Body:
    # Initial values
    To = 0
    po = 2/3 * np.sqrt(ro*ro*ro/rs) + To

    dₛTo = np.sqrt(1/(1 - 3/2 * (2/3 * rs/po)**(2/3)))
    dₛpo = dₛTo
    dₛφo = np.sqrt(2/9 * dₛpo * dₛpo/(po*po))
    dₛφo = h/(ro*ro)

    pos = [0, po, np.pi/2, 0]
    vel = [dₛTo, dₛpo, 0, dₛφo]
    if verbose == 1: print(f"h={h}")

    # Metric config
    coordinates = Lemaitre
    T, ρ, θ, φ = Lemaitre.coords
    r = (3/2 * (ρ - T))**(2/3) * rs**(1/3)

    gₘₖ = Matrix([
        [1     ,0     ,0          ,0          ],
        [0     ,-rs/r  ,0          ,0          ],
        [0     ,0     ,-r**2      ,0          ],
        [0     ,0     ,0          ,-r**2 * sin(θ)**2]
    ])


    # Solver config
    if sim_T is None: sim_T = 2*np.pi*(2*ro*ro*ro/rs)**(1/2) # Third law of Kepler
    solver_kwargs = {
        "time_interval": (0,sim_T),           
        "method"       : "Radau",          
        "max_step"     : sim_T*1e-3,
        "atol"         : 1e-8,              
        "rtol"         : 1e-8,              
        "events"       : None,              
    }

    # Basic run config
    args_basic = {
        "coordinates"  : coordinates,
        "g_mk"         : gₘₖ, 
        "initial_pos"  : pos, 
        "initial_vel"  : vel, 
        "simplify"     : True,
        "solver_kwargs": solver_kwargs, 
        "verbose"      : verbose, 
    }
    body = basic(**args_basic)

    # Output options
    orbit_plot_title:  str  = output_kwargs.get("orbit_plot_title" , "Trajectory of a star orbiting a blackhole")
    orbit_pdf_name:    str  = output_kwargs.get("orbit_pdf_name"   , "o_schwarzschild.pdf")
    orbit_mp4_name:    str  = output_kwargs.get("orbit_mp4_name"   , "o_schwarzschild.mp4")
    velocity_pdf_name: str  = output_kwargs.get("velocity_pdf_name", "v_schwarzschild.pdf") 
    plot_orbit:        bool = output_kwargs.get("plot_orbit"       , False        )
    animate:           bool = output_kwargs.get("animate"          , False        )
    plot_velocity:     bool = output_kwargs.get("plot_velocity"    , False        )
    save_pdf:          bool = output_kwargs.get("save_pdf"         , False        )
    save_mp4:          bool = output_kwargs.get("save_mp4"         , False        )
    v_save_pdf:        bool = output_kwargs.get("v_save_pdf"       , False        )  
    assert not (save_pdf   and not plot_orbit   )
    assert not (save_mp4   and not animate      )
    assert not (v_save_pdf and not plot_velocity)

    # Plotting
    body = body.get_spherical_body(rs=rs)
    plotter = PolarPlot(body)

    if plot_orbit:    plotter.plot(title=orbit_plot_title)
    if animate:       plotter.animate()
    if plot_velocity:
        body.calculate_velocities()
        plotter.plot_velocity("Velocity")

    # Drawing blackhole
    plotter.add_circle((0,0), rs, edgecolor="k", fill=True, facecolor='k')

    # Create outputs directory if doesn't exist.
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Save plots
    if save_pdf:   plotter.save_plot("outputs/" + orbit_pdf_name)
    if save_mp4:   plotter.save_animation("outputs/" + orbit_mp4_name, dpi=300)
    if v_save_pdf: plotter.save_plot_velocity("outputs/" + velocity_pdf_name)

    plotter.show()
    return body


def main():
    print("WARNING -> This file is meant to be used as a module for the other files in this directory. By itself, no calculations are done. To compute the geodesics of this metric with given initial parameters, run the other files in this directory.")
    print("Exiting.")

if __name__ == "__main__":
    main()
