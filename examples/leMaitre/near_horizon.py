import numpy as np
from leMaitre import leMaitre, hcirc

# Initial values
rs = 1 
ro = 5
h = hcirc(rs,ro)

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "o_schwarzschild.pdf",
    "orbit_mp4_name"   : "o_schwarzschild.mp4",
    "velocity_pdf_name": "v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

leMaitre(rs=rs, ro=ro, h=h, sim_T=None, output_kwargs=output_kwargs, verbose=1)
