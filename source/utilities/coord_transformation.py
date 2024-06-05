import numpy as np
from scipy.integrate._ivp.ivp import OdeResult
import matplotlib.pyplot as plt

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

def spherical_to_cartesian(ode_result: OdeResult):
    new_coordinates = []
    """
    x = lambda r, θ, φ: r * np.sin(θ) * np.cos(φ)
    y = lambda r, θ, φ: r * np.sin(θ) * np.sin(φ)
    z = lambda r, θ, φ: r * np.cos(θ)
    """
    
    r, θ, φ = ode_result.y[1:4]

    print(r, θ, φ)
    print(type(r))
    x = r * np.sin(θ) * np.cos(φ)
    y = r * np.sin(θ) * np.sin(φ)
    z = r * np.cos(θ)

    return x, y, z
