import numpy as np
from sitter_schwarzschild import sitter_schwarzschild, kcirc, hcirc

# Initial values
rs = 1 
ro = 5
k, h = kcirc(rs, ro), hcirc(rs, ro)
h -= 0.1
Λ = 1.11e-52

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "o_schwarzschild.pdf",
    "orbit_mp4_name"   : "o_schwarzschild.mp4",
    "velocity_pdf_name": "v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : True,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

sitter_schwarzschild(rs=rs, ro=ro, h=h, k=k, Λ=1.11e-52, T=None, output_kwargs=output_kwargs, verbose=1)
