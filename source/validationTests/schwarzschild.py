import numpy as np

# Energy check (k)
def check_k(r_values: list[float], dₛt_values: list[float], rs: float, tol: float = 0.00001) -> bool:
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
def check_h(r_values: list[float], dₛφ_values: list[float], rs: float, tol: float = 0.00001) -> bool:
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
