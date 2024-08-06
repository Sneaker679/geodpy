import numpy as np
from .. import Body

# Energy check (k)
def check_k(body: Body, rs: float, tol: float = 0.00001) -> None:
    r_values   = body.pos[1]
    dₛt_values = body.vel[0]

    dₛt_init  = dₛt_values[0]
    r_init    = r_values[0]
    k_init    = dₛt_init * (1 - rs/r_init)

    check = True
    for dₛt, r in zip(dₛt_values, r_values):
        k = dₛt * (1 - rs/r)
        if np.abs(k_init - k) > tol:
            check = False
            break

    print(f"Energy conserved: {check}")

# Angular momentum check (h)
def check_h(body: Body, rs: float, tol: float = 0.00001) -> None:
    r_values   = body.pos[1]
    dₛφ_values = body.vel[3]

    dₛφ_init = dₛφ_values[0]
    r_init    = r_values[0]
    h_init = r_init * r_init * dₛφ_init

    check = True
    for dₛφ, r in zip(dₛφ_values, r_values):
        h = r*r * dₛφ
        if np.abs(h_init - h) > tol:
            check = False
            break

    print(f"Angular momentum conserved: {check}")
