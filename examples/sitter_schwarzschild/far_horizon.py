import numpy as np
from sitter_schwarzschild import sitter_schwarzschild, kcirc, hcirc

# Initial values
rs = 1e-1
ro = 5e15
k, h = kcirc(rs, ro), hcirc(rs, ro)
Λ = 0#-1.11e-52 

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "outputs/o_schwarzschild.pdf",
    "orbit_mp4_name"   : "outputs/o_schwarzschild.mp4",
    "velocity_pdf_name": "outputs/v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : False,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

sitter_schwarzschild(rs=rs, ro=ro, h=h, k=k, Λ=Λ, T=None, output_kwargs=output_kwargs, verbose=1)
