from geodpy import Geodesics, Body, basic
from geodpy.plotters import PolarPlot, CartesianPlot2D
from geodpy.coordinates import Spherical

from sympy import *
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

import os

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# Returns k for a circular orbit
def kcirc(rs, r) -> float:
    return (1-rs/r)/np.sqrt(1-3*rs/(2*r))

# Returns h for a circular orbit
def hcirc(rs, r) -> float:
    return np.sqrt(rs*r/(2-3*rs/r))

# Schwarzschild example function
def schwarzschild(rs: float, ro: float, h: float, k: float, T: float|None = None, output_kwargs: dict = {}, verbose: int = 1) -> Body:
    # Initial values
    pos = [0, ro, np.pi/2, 0]
    vel = [k/(1-rs/ro), 0, 0, h/(ro**2)]
    if verbose == 1: print(f"h={h}, k={k}")

    # Metric config
    coordinates = Spherical
    t, r, θ, φ = Spherical.coords

    gₘₖ = Matrix([
        [1-rs/r     ,0          ,0          ,0          ],
        [0          ,1/(rs/r-1) ,0          ,0          ],
        [0          ,0          ,-r**2      ,0          ],
        [0          ,0          ,0          ,-r**2 * sin(θ)**2]
    ])


    # Solver config
    if T is None: T = 2*np.pi*(2*ro*ro*ro/rs)**(1/2) # Third law of Kepler
    solver_kwargs = {
        "time_interval": (0,T),           
        "method"       : "Radau",          
        "max_step"     : T*1e-3,
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
        "solver_kwargs": solver_kwargs, 
        "verbose"      : verbose, 
    }
    body = basic(**args_basic)

    # Output options
    orbit_plot_title:  str  = output_kwargs.get("orbit_plot_title" , "Trajectory of a star orbiting a blackhole")
    orbit_pdf_name:    str  = output_kwargs.get("orbit_pdf_name"   , "o_schwarzschild.pdf")
    orbit_mp4_name:    str  = output_kwargs.get("orbit_mp4_name"   , "o_schwarzschild.mp4")
    velocity_pdf_name: str  = output_kwargs.get("velocity_pdf_name", "v_schwarzschild.pdf") 
    plot_orbit:        bool = output_kwargs.get("plot_orbit"       , True         )
    animate:           bool = output_kwargs.get("animate"          , False        )
    plot_velocity:     bool = output_kwargs.get("plot_velocity"    , False        )
    save_pdf:          bool = output_kwargs.get("save_pdf"         , False        )
    save_mp4:          bool = output_kwargs.get("save_mp4"         , False        )
    v_save_pdf:        bool = output_kwargs.get("v_save_pdf"       , False        )  
    assert not (save_pdf   and not plot_orbit   )
    assert not (save_mp4   and not animate      )
    assert not (v_save_pdf and not plot_velocity)

    # Plotting
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
    if save_pdf:   plotter.save_plot(orbit_pdf_name)
    if save_mp4:   plotter.save_animation(orbit_mp4_name, dpi=300)
    if v_save_pdf: plotter.save_plot_velocity(velocity_pdf_name)

    plotter.show()
    return body


def main():
    print("WARNING -> This file is meant to be used as a module for the other files in this directory. By itself, no calculations are done. To compute the geodesics of this metric with given initial parameters, run the other files in this directory.")
    print("Exiting.")

if __name__ == "__main__":
    main()
