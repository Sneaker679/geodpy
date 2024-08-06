import numpy as np
from lemaitre import lemaitre, hcirc

# Initial values
rs = 1 
ro = 5
h = hcirc(rs,ro)
h -= 0.108082

output_kwargs = {
    "orbit_plot_title" : "Star crashing into a blackhole",
    "orbit_pdf_name"   : "o_lemaitre.pdf",
    "orbit_mp4_name"   : "o_lemaitre.mp4",
    "velocity_pdf_name": "v_lemaitre.pdf",
    "plot_orbit"       : True,
    "animate"          : True,
    "plot_velocity"    : False,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

lemaitre(rs=rs, ro=ro, h=h, sim_T=150, output_kwargs=output_kwargs, verbose=1)
