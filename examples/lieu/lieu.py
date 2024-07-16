from geodpy import Geodesics, Body, basic
from geodpy.plotters import PolarPlot, CartesianPlot2D
from geodpy.coordinates import Spherical

from sympy import *
import numpy as np

import os

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

def hcirc(r: float, α: float = 10e-6):
    return r * np.sqrt(α/(1 + α*(np.log(r) - 1)))

def kcirc(r: float, α: float = 10e-6):
    return ((1 + α * np.log(r))**(3/2)) / (1 + α * (np.log(r) - 1))

# Lieu example function
def lieu(ro: float, h: float, k: float, α: float = 10e-6, T: float|None = None, output_kwargs: dict = {}, verbose: int = 1) -> Body:
    # Initial values
    pos = [0, ro, np.pi/2, 0]
    vel = [k/((1+α*np.log(ro)**2)), 0, 0, h/(ro**2)]

    # Metric config
    coordinates = Spherical
    t, r, θ, φ = Spherical.coords

    gₘₖ = Matrix([
        [(1 + α*ln(r))**2,0          ,0          ,0          ],
        [0               ,-(1 + α)**2,0          ,0          ],
        [0               ,0          ,-r**2      ,0          ],
        [0               ,0          ,0          ,-r**2 * sin(θ)**2]
    ])

    # Solver config
    if T is None: T = 2 * np.pi * ro /(np.sqrt(α) * np.sqrt(1 + α * np.log(ro))) # Third law of Kepler
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
        "simplify"     : True
        "solver_kwargs": solver_kwargs, 
        "verbose"      : verbose, 
    }
    body = basic(**args_basic)

    # Output options
    orbit_plot_title:  str  = output_kwargs.get("orbit_plot_title" , "Trajectory of a star orbitting a galaxy.")
    orbit_pdf_name:    str  = output_kwargs.get("orbit_pdf_name"   , "o_lieu.pdf")
    orbit_mp4_name:    str  = output_kwargs.get("orbit_mp4_name"   , "o_lieu.mp4")
    velocity_pdf_name: str  = output_kwargs.get("velocity_pdf_name", "v_lieu.pdf") 
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
