import numpy as np
from schwarszchild import schwarzschild, kcirc, hcirc

# Initial values
rs = 2954
ro = 151_820_000_000
k = 1.000000005
h = 14_857_341

output_kwargs = {
    "orbit_pdf_name"   : "outputs/o_schwarzschild.pdf",
    "orbit_mp4_name"   : "outputs/o_schwarzschild.mp4",
    "velocity_pdf_name": "outputs/o_schwarzschild.mp4",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

schwarzschild(rs=rs, ro=ro, h=h, k=k, T=9.455454125e15, output_kwargs=output_kwargs, verbose=1)
