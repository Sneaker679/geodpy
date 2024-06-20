import numpy as np
from sitter_schwarzschild import sitter_schwarzschild, kcirc, hcirc, velocity_circ

m_sun = 1.9884e30
G = 6.67430e-11
c = 3e8
al = 9.4607e15 #meters

# Milky way
M_galaxy = m_sun*1.15e12
rs = 2*M_galaxy*G/(c*c)
print(rs)
ro = 50_000 * al

output_kwargs = {
    "orbit_plot_title" : "Trajectory of a star orbiting a blackhole",
    "orbit_pdf_name"   : "outputs/o_schwarzschild.pdf",
    "orbit_mp4_name"   : "outputs/o_schwarzschild.mp4",
    "velocity_pdf_name": "outputs/v_schwarzschild.pdf",
    "plot_orbit"       : True,
    "animate"          : False,
    "plot_velocity"    : True,
    "save_pdf"         : False,
    "save_mp4"         : False,
    "v_save_pdf"       : False  
}

#T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro))
# Positive lambda
Λ = 1.11e-52 
k, h = kcirc(rs, ro, Λ), hcirc(rs, ro, Λ)
T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro) - Λ/3)
body_pos = sitter_schwarzschild(rs=rs, ro=ro, h=h, k=k, Λ=Λ, T=T, output_kwargs=output_kwargs, verbose=1)
v_pos = velocity_circ(rs, ro, Λ)

# Null lambda
Λ = 0 
k, h = kcirc(rs, ro, Λ), hcirc(rs, ro, Λ)
T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro) - Λ/3)
body_0 = sitter_schwarzschild(rs=rs, ro=ro, h=h, k=k, Λ=Λ, T=T, output_kwargs=output_kwargs, verbose=1)
v_0 = velocity_circ(rs, ro, Λ)

# Negative lambda
Λ = -1.11e-52 
k, h = kcirc(rs, ro, Λ), hcirc(rs, ro, Λ)
T = 2*np.pi/np.sqrt(rs/(2*ro*ro*ro) - Λ/3)
body_neg = sitter_schwarzschild(rs=rs, ro=ro, h=h, k=k, Λ=Λ, T=T, output_kwargs=output_kwargs, verbose=1)
v_neg = velocity_circ(rs, ro, Λ)

#T = 2*np.pi*np.sqrt(2*ro*ro*ro/rs)

print("Period:")
print(body_pos.pos[0][-1]/c)
print(body_0.pos[0][-1]/c)
print(body_neg.pos[0][-1]/c)
print("Final angle after one period:")
print(body_pos.pos[3][-1] - 2*np.pi)
print(body_0.pos[3][-1] - 2*np.pi)
print(body_neg.pos[3][-1] - 2*np.pi)
print("Mean velocity:")
print(np.mean(body_pos.vel_norm[20:-1])*c)
print(np.mean(body_0.vel_norm[20:-1])*c)
print(np.mean(body_neg.vel_norm[20:-1])*c)
print("Exact velocity:")
print(v_pos*c)
print(v_0*c)
print(v_neg*c)
