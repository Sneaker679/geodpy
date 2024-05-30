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

gₘₖ = Matrix([
    [1-1/r      ,0          ,0          ,0          ],
    [0          ,(1/r-1)**-1,0          ,0          ],
    [0          ,0          ,-r**2      ,0          ],
    [0          ,0          ,0          ,-r**2 * sin(θ)**2]
])


if __name__ == "__main__":
    dₛuⱼ= simplify(covariant_acc(s, gₘₖ, coordinates))
    pprint(dₛuⱼ)

    print()
    print()
    print()

    dₛuʲ= simplify(contravariant_acc(s, gₘₖ, coordinates))
    pprint(dₛuʲ)
