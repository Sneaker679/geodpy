import numpy as np
from lieu import lieu, kcirc, hcirc

# Initial values
α = 10e-6
ro = 1e6
k, h = kcirc(ro, α), hcirc(ro, α)

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a galaxy",
    "orbit_pdf_name"   : "o_lieu.pdf",
    "orbit_mp4_name"   : "o_lieu.mp4",
    "velocity_pdf_name": "v_lieu.pdf",
    "plot_orbit"       : True,
    "animate"          : False,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

lieu(ro=ro, h=h, k=k, α=α, T=None, output_kwargs=output_kwargs, verbose=1)
