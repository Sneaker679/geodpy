import numpy as np
from kerr import kerr, circ

# Initial values
rs = 2 
ro = 7
a = 0.9
σ = -1 #1 or -1
assert a < rs/2
k, h = circ(rs, ro, a, σ)
h += -1.5

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star falling into a rotating blackhole",
    "orbit_pdf_name"   : "o_kerr.pdf",
    "orbit_mp4_name"   : "o_kerr.mp4",
    "velocity_pdf_name": "v_kerr.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

kerr(rs=rs, ro=ro, h=h, k=k, a=a, θ_init=np.pi/4, T=6000, output_kwargs=output_kwargs, verbose=1, dim=3)
