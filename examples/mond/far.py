import numpy as np
from mond import mond, kcirc, hcirc

# Initial values
M = 1 
ro = 1e9
ao = np.sqrt(1.11e-52/3)
k, h = kcirc(M, ro, ao=ao), hcirc(M, ro, ao=ao)

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "o_schwarzschild.pdf",
    "orbit_mp4_name"   : "o_schwarzschild.mp4",
    "velocity_pdf_name": "v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : False,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

mond(M=M, ro=ro, h=h, k=k, ao=ao, T=5e16, output_kwargs=output_kwargs, verbose=1)
