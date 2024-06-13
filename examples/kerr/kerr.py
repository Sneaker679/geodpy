from geodpy import Geodesics, Body, basic, BodyPlotter, Spherical

from sympy import *
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# Possible symbols
#τ,t,r,a,b,c,θ,φ,η,ψ,x,y 

def circ(rs: float, r: float, a: float, σ: int) -> tuple[float,float]:
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

def kerr(rs: float, ro: float, h: float, k: float, a: float, θ: float = np.pi/2, T: float|None = None, output_kwargs: dict = {}, verbose: int = 1) -> None:
    # Initial values
    dₛt = contravariant_tdot(ro, rs, a, k, h)
    dₛr = contravariant_rdot2(ro, rs, a, k, h)
    dₛφ = contravariant_phidot(ro, rs, a, k, h)
    pos = [0, ro, θ, 0]
    vel = [dₛt, dₛr, 0, dₛφ] 
    if verbose == 1: print(f"h={h}, k={k}, a={a}")

    # Metric config
    coordinates = Spherical
    t, r, θ, φ = Spherical.coords

    gₘₖ = Matrix([
        [1-rs*r/(p*p)             ,0      ,0    ,(a*r*rs*sin(θ)**2)/(p*p)                            ],
        [0                        ,-p*p/Δ ,0    ,0                                                   ],
        [0                        ,0      ,-p*p ,0                                                   ],
        [(a*r*rs*sin(θ)**2)/(p*p) ,0      ,0    ,-(r*r + a*a + (a*a*r*rs*sin(θ)**2)/(p*p))*sin(θ)**2]
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
    orbit_plot_title:  str  = output_kwargs.get("orbit_plot_title" , "Trajectory of a star orbiting a rotating blackhole")
    orbit_pdf_name:    str  = output_kwargs.get("orbit_pdf_name"   , "outputs/o_kerr.pdf")
    orbit_mp4_name:    str  = output_kwargs.get("orbit_mp4_name"   , "outputs/o_kerr.mp4")
    velocity_pdf_name: str  = output_kwargs.get("velocity_pdf_name", "outputs/v_kerr.pdf") 
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
    ps = []
    r_ext, r_int = radii(rs, a) 
    ps.append(patches.Circle((0,0), r_ext, edgecolor="k", fill=True, facecolor='k')) # blackhole ext
    ps.append(patches.Circle((0,0), r_int, edgecolor="b")) # blackhole int
    plotter = BodyPlotter(body)
    plotter.set_patches(ps)

    if plot_orbit:    plotter.plot(title=orbit_plot_title)
    if animate:       plotter.animate()
    if plot_velocity:
        body.calculate_velocities()
        plotter.plot_velocity("Velocity")

    if save_pdf:   plot.save_plot(orbit_pdf_name)
    if save_mp4:   plot.save_animation(orbit_mp4_name)
    if v_save_pdf: plot.save_plot_velocity(velocity_pdf_name)

    plotter.show()
    return body
