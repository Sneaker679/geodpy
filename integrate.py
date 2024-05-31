

def diff_equations_system(dτ, state, equations : list):
    assert len(equations) == 4
    x0, x1, x2, x3, v0, v1, v2, v3  = state

    a0 = equations[0](x0, x1, x2, x3, v0, v1, v2, v3)
    a1 = equations[1](x0, x1, x2, x3, v0, v1, v2, v3)
    a2 = equations[2](x0, x1, x2, x3, v0, v1, v2, v3)
    a3 = equations[3](x0, x1, x2, x3, v0, v1, v2, v3)
    
    return v0, v1, v2, v3, a0, a1, 0, a3
