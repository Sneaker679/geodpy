from sympy import *
import numpy as np
from to_lambda import vector_to_lambda

class Geodesics:

    def __init__(self, s : Symbol, gₘₖ: Matrix, coordinates: list[Function]):
        assert gₘₖ.shape[0] == len(coordinates)
        assert s not in coordinates
        
        self._s = s
        self._gₘₖ= gₘₖ
        self._coordinates = coordinates
        self._dₛuᵏ= self.__contravariant_acc()
        self._dₛuᵏ_lambda = vector_to_lambda(s, self._dₛuᵏ, coordinates)

    # Geodesic covariant equation : ∂ₛuⱼ = 1/2 * ∂ⱼ(gₘₖ) * uᵐ uᵏ where uᵏ = ∂ₛxᵏ 
    def __covariant_acc(self) -> Array:
        dₛuⱼ: list[Function] = []
        uᵐ  : Array = Array(self._coordinates).diff(self._s)
        uᵐuᵏ: Array = tensorproduct(uᵐ,uᵐ)

        for j, coord in enumerate(self._coordinates):
            dₛuⱼ.append(1/2 * tensorcontraction(tensorproduct(self._gₘₖ.diff(coord), uᵐuᵏ), (0,1,2,3)))
        
        dₛuⱼ= Array(dₛuⱼ)
        return dₛuⱼ

    # Geodesic contravariant equation : ∂ₛuᵏ = gᵐᵏ(∂ₛuₘ - ∂ₛgₘⱼuʲ) where uᵏ = ∂ₛxᵏ
    def __contravariant_acc(self) -> Array:
        dₛuₘ_: Array  = self.__covariant_acc()
        gᵐᵏ_ : Matrix = self._gₘₖ.inv()
        uʲ   : Array  = Array(self._coordinates).diff(self._s)
        
        dₛgₘⱼuʲ= tensorcontraction(tensorproduct( self._gₘₖ.diff(self._s), uʲ              ), (1,2))
        dₛuᵏ   = tensorcontraction(tensorproduct( gᵐᵏ_                   , dₛuₘ_ - dₛgₘⱼuʲ ), (1,2))
        
        return dₛuᵏ

