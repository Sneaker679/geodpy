from sympy import *

# Geodesic covariant equation : ∂ₛuⱼ = 1/2 * ∂ⱼ(gₘₖ) * uᵐ uᵏ where uᵏ = ∂ₛxᵏ 
def covariant_acc(s : Symbol, gₘₖ: Matrix, coordinates: list[Function]) -> Array:
    assert gₘₖ.shape[0] == len(coordinates)
    dₛuⱼ: list[Function] = []
    uᵐ  : Array = Array(coordinates).diff(s)
    uᵐuᵏ: Array = tensorproduct(uᵐ,uᵐ)

    for j, coord in enumerate(coordinates):
        dₛuⱼ.append(1/2 * tensorcontraction(tensorproduct(gₘₖ.diff(coord), uᵐuᵏ), (0,1,2,3)))
    
    dₛuⱼ= Array(dₛuⱼ)
    return simplify(dₛuⱼ)

# Geodesic contravariant equation : ∂ₛuᵏ = ∂ₛ(gᵐᵏuₘ) = g where uᵏ = ∂ₛxᵏ
def contravariant_acc(s : Symbol, gₘₖ: Matrix, coordinates: list[Function]) -> Array:
    assert gₘₖ.shape[0] == len(coordinates)
    dₛuₘ_: Array  = covariant_acc(s, gₘₖ, coordinates)
    gᵐᵏ_ : Matrix = gₘₖ.inv()
    uʲ   : Array  = Array(coordinates).diff(s)
    
    gₘⱼuʲ= tensorcontraction(tensorproduct( gₘₖ.diff(s), uʲ            ), (1,2))
    dₛuᵏ = tensorcontraction(tensorproduct( gᵐᵏ_       , dₛuₘ_ - gₘⱼuʲ ), (1,2))
    
    return simplify(dₛuᵏ)

# Converts contravariant or covariant accelerations tensor arrays into lambda expressions, for later integration
def to_lambda(s : Symbol, expressions : Array, coordinates : list[Function]):
    assert expressions.shape[0] == len(coordinates)
    dₛcoordinates : list[Function] = [coord.diff(s) for coord in coordinates]
    coordinates.extend(dₛcoordinates)

    lambda_functions : list[Function] = []
    for k, expr in enumerate(expressions):
        lambda_functions.append(lambdify(coordinates, expr, "scipy"))
    return lambda_functions
