import numpy as np
from schwarszchild import schwarzschild, kcirc, hcirc
from geodpy.plotters import PolarPlot

# Initial values
rs = 2954
ro = 151_820_000_000
k = 1.000000005
h = 14_857_341

# Output parameters
orbit_plot_title  = "Elliptical orbit of Earth"
orbit_pdf_name    = "o_earth_ellipse.pdf"
orbit_mp4_name    = "o_earth_ellipse.mp4"
velocity_pdf_name = "v_earth_ellipse.pdf"
plot_orbit        = True
animate           = True
plot_velocity     = False
save_pdf          = False
save_mp4          = False
v_save_pdf        = False  

body = schwarzschild(rs=rs, ro=ro, h=h, k=k, T=9.455454125e15, verbose=1)


# Plotting
plotter = PolarPlot(body)

if plot_orbit:    plotter.plot(title=orbit_plot_title)
if animate:       plotter.animate()
if plot_velocity:
    body.calculate_velocities()
    plotter.plot_velocity("Velocity")

# Drawing Sun
plotter.add_circle((0,0), 1.3914e9, edgecolor="y", fill=True, facecolor='y')

# Save plots
if save_pdf:   plotter.save_plot(orbit_pdf_name)
if save_mp4:   plotter.save_animation(orbit_mp4_name, dpi=300)
if v_save_pdf: plotter.save_plot_velocity(velocity_pdf_name)

plotter.show()
