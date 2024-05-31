from sympy import *
from geodesics import *

# Possible symbols
#t,r,a,b,c,θ,φ,η,ψ,x,y 

# Interval conf
s = symbols('s')

# Metric conf
# EX : Schwarzschild metric
t = Function('t')(s)
r = Function('r')(s)
θ = Function('θ')(s)
φ = Function('φ')(s)
coordinates : list[Function] = [t, r, θ, φ]

rs = 1
gₘₖ = Matrix([
    [1-rs/r     ,0          ,0          ,0          ],
    [0          ,1/(rs/r-1) ,0          ,0          ],
    [0          ,0          ,-r**2      ,0          ],
    [0          ,0          ,0          ,-r**2 * sin(θ)**2]
])


if __name__ == "__main__":
    dₛuⱼ= simplify(covariant_acc(s, gₘₖ, coordinates))
    dₛuʲ= simplify(contravariant_acc(s, gₘₖ, coordinates))
    pprint(dₛuʲ)
    equations : list = to_lambda(s, dₛuʲ,coordinates)

    # Integration
    from scipy.integrate import solve_ivp
    from integrate import *
    import numpy as np
    ro = 4
    initial = [0,ro,pi/2,0,3/(1-rs/ro),0,0,np.sqrt(3/(ro**2))-0.05]
    values = solve_ivp(fun = diff_equations_system, t_span = (0,200), max_step = 0.1, y0 = initial, args=(equations,))
    print(values)


    # Checking is quantities are conserved
    tol = 0.00001

    # Energy (k)
    dotT_init = values.y[4][0]
    r_init = values.y[1][0]
    k_init = dotT_init * (1 - rs/r_init)
    for dotT, r in zip(values.y[4], values.y[1]):
        k = dotT*(1-rs/r)
        assert np.abs(k_init - k) < tol
    print("Energy is conserved.")

    # Angular momentum (h)
    dotPhi_init = values.y[7][0]
    h_init = r_init**2 * dotPhi_init
    for dotPhi, r in zip(values.y[7], values.y[1]):
        h = r**2 * dotPhi
        assert np.abs(h_init - h) < tol
    print("Angular momentum conserved.")


    # Plotting
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    x = []
    y = []
    for r,phi in zip(values.y[1],values.y[3]):
        x.append(r*np.cos(phi))
        y.append(r*np.sin(phi))
    #plt.plot(values.t, values.y[1])
    
    fig, ax = plt.subplots()
    ax.add_patch(patches.Circle((0,0), 1, edgecolor="black", fill=True))

    plt.plot(x,y)
    fig.set_size_inches(20, 20,forward=True)
    plt.xlim(-16,16)
    plt.ylim(-16,16)
    fig.savefig("schwarzschild.pdf")
    plt.show()


