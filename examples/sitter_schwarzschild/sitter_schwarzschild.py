from geodpy import Geodesics, Body, basic, PolarPlot, Spherical

from sympy import *
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

import os

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

# Returns the velocity a body should have on a circular orbit. Used for comparaisons. Not used in this file.
def velocity_circ(rs, r, Λ=1.11e-52):
    return np.sqrt((rs - 2*Λ*r*r*r/3)/(2*r-3*rs))

# Returns k for a circular orbit
def kcirc(rs, r, Λ=1.11e-52) -> float:
    return (1-rs/r-Λ*r*r/3)/np.sqrt(1-3*rs/(2*r))

# Returns h for a circular orbit
def hcirc(rs, r, Λ=1.11e-52) -> float:
    return np.sqrt((rs/(2*r*r*r) - Λ/3)/((1/(r*r*r*r))*(1-3*rs/(2*r))))

# Sitter Schwarzschild example function
def sitter_schwarzschild(rs: float, ro: float, h: float, k: float, Λ: float = 1.11e-52, T: float|None = None, output_kwargs: dict = {}, verbose: int = 1) -> Body:
    # Initial values
    pos = [0, ro, np.pi/2, 0]
    vel = [k/(1-rs/ro), 0, 0, h/(ro**2)]
    if verbose == 1: print(f"h={h}, k={k}, Λ={Λ}")

    # Metric config
    coordinates = Spherical
    t, r, θ, φ = Spherical.coords

    gₘₖ = Matrix([
        [1-rs/r - Λ*r*r/3 ,0                    ,0          ,0                ],
        [0                ,1/(Λ*r*r/3 + rs/r-1) ,0          ,0                ],
        [0                ,0                    ,-r**2      ,0                ],
        [0                ,0                    ,0          ,-r**2 * sin(θ)**2]
    ])

    # Solver config
    if T is None: T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro) - Λ/3)
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
