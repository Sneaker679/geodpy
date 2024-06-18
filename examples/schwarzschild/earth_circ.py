import numpy as np
from schwarszchild import schwarzschild, kcirc, hcirc

# Initial values
rs = 2954
ro = 151_820_000_000
k, h = kcirc(rs, ro), hcirc(rs, ro)

output_kwargs = {
    "orbit_plot_title" : "Circular orbit of Earth",
    "orbit_pdf_name"   : "outputs/o_earth_circ.pdf",
    "orbit_mp4_name"   : "outputs/o_earth_circ.mp4",
    "velocity_pdf_name": "outputs/v_earth_circ.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

schwarzschild(rs=rs, ro=ro, h=h, k=k, T=9.455454125e15, output_kwargs=output_kwargs, verbose=1)
