from geodesics import Geodesics
from body import Body
from basic import basic
from utilities.bodyplotter import BodyPlotter

from sympy import *
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

def kcirc(rs, r) -> float:
    return (1-rs/r)/np.sqrt(1-3*rs/(2*r))

def hcirc(rs, r) -> float:
    return np.sqrt(rs*r/(2-3*rs/r))

def schwarzschild(rs, ro, h, k, output_kwargs: dict = {}, verbose: int = 0) -> None:
    # Initial values
    pos = [0, ro, np.pi/2, 0]
    vel = [k/(1-rs/ro), 0, 0, h/(ro*ro)]

    # Metric config
    s = symbols('s')
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


    # Solver config
    T = 2*np.pi*(2*ro*ro*ro/rs)**(1/2) # Third law of Kepler
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
        "s"            : symbols('s'), 
        "coordinates"  : coordinates,
        "g_mk"          : gₘₖ, 
        "initial_pos"  : pos, 
        "initial_vel"  : vel, 
        "solver_kwargs": solver_kwargs, 
        "verbose"      : 1, 
    }
    body = basic(**args_basic)

    # Output options
    orbit_pdf_name:    str  = output_kwargs.get("orbit_pdf_name"   , "outputs/o_schwarzschild.pdf")
    orbit_mp4_name:    str  = output_kwargs.get("orbit_mp4_name"   , "outputs/o_schwarzschild.mp4")
    velocity_pdf_name: str  = output_kwargs.get("velocity_pdf_name", "outputs/o_schwarzschild.mp4") 
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
    ps = [patches.Circle((0,0), rs, edgecolor="k", fill=True, facecolor='k')] # blackhole
    plotter = BodyPlotter(body)
    plotter.set_polar()
    plotter.set_patches(ps)

    if plot_orbit:    plotter.plot(title="Trajectory of a star orbiting a blackhole")
    if animate:       plotter.animate()
    if plot_velocity: plotter.plot_velocity("velocity")

    if save_pdf:   plot.save_plot(orbit_pdf_name)
    if save_mp4:   plot.save_animation(orbit_mp4_name)
    if v_save_pdf: plot.save_plot_velocity(velocity_pdf_name)

    plotter.show()
