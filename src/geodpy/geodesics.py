from .to_lambda import vector_to_lambda
from .coordinates import Coordinates

from sympy import *
import numpy as np

### Geodesic class ###
# Class that acts as a variables container for all geodesics.
class Geodesics:

    def __init__(self, coordinates: Coordinates, gₘₖ: Matrix):
        assert gₘₖ.shape[0] == len(coordinates.coords)
        
        # Automatic calculation of all geodesics variables
        self._coordinates = coordinates
        self._gₘₖ= gₘₖ
        self._dₛuᵏ= self.__contravariant_acc()
        self._dₛuᵏ_lambda = vector_to_lambda(coordinates, self._dₛuᵏ)

    # Geodesic covariant equation : ∂ₛuⱼ = 1/2 * ∂ⱼ(gₘₖ) * uᵐ uᵏ where uᵏ = ∂ₛxᵏ 
    def __covariant_acc(self) -> Array:
        dₛuⱼ: list[Function] = []
        uᵐ  : Array = Array(self._coordinates.coords).diff(self._coordinates.interval)
        uᵐuᵏ: Array = tensorproduct(uᵐ,uᵐ)

        for j, coord in enumerate(self._coordinates.coords):
            dₛuⱼ.append(1/2 * tensorcontraction(tensorproduct(self._gₘₖ.diff(coord), uᵐuᵏ), (0,1,2,3)))
        
        return Array(dₛuⱼ)

    # Geodesic contravariant equation : ∂ₛuᵏ = gᵐᵏ(∂ₛuₘ - ∂ₛgₘⱼuʲ) where uᵏ = ∂ₛxᵏ
    def __contravariant_acc(self) -> Array:
        dₛuₘ_: Array  = self.__covariant_acc()
        gᵐᵏ_ : Matrix = self._gₘₖ.inv()
        uʲ   : Array  = Array(self._coordinates.coords).diff(self._coordinates.interval)
        
        dₛgₘⱼuʲ= tensorcontraction(tensorproduct( self._gₘₖ.diff(self._coordinates.interval), uʲ             ), (1,2))
        dₛuᵏ   = tensorcontraction(tensorproduct( gᵐᵏ_                                      , dₛuₘ_ - dₛgₘⱼuʲ), (1,2))
        
        return dₛuᵏ

    def simplify(self):
        self._dₛuᵏ= simplify(self._dₛuᵏ)
        self._dₛuᵏ_lambda = vector_to_lambda(self._coordinates, self._dₛuᵏ)

