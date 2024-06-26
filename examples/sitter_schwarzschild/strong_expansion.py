import numpy as np
from sitter_schwarzschild import sitter_schwarzschild, kcirc, hcirc

# Initial values
rs = 1 
ro = 1e13 #1.95e17
Λ = 1e-40
k, h = kcirc(rs, ro, Λ=Λ), hcirc(rs, ro, Λ=Λ)
T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro) - Λ/3)*6.5

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "o_schwarzschild.pdf",
    "orbit_mp4_name"   : "o_schwarzschild.mp4",
    "velocity_pdf_name": "v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : True,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

sitter_schwarzschild(rs=rs, ro=ro*2.000001, h=h, k=k, Λ=Λ, T=T, output_kwargs=output_kwargs, verbose=1)
