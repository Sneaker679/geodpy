import numpy as np
from kerr import kerr, circ

# Initial values
rs = 1 
ro = 5
a = 0 #0.495
σ = -1 #1 or -1
assert a < rs/2
k, h = circ(rs, ro, a, σ)
h += 1

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a rotating blackhole",
    "orbit_pdf_name"   : "outputs/o_kerr.pdf",
    "orbit_mp4_name"   : "outputs/o_kerr.mp4",
    "velocity_pdf_name": "outputs/v_kerr.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

kerr(rs=rs, ro=ro, h=h, k=k, a=a, θ=np.pi/2, T=500, output_kwargs=output_kwargs, verbose=1)