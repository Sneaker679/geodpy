# vector\_to\_lambda()
DESCRIPTION: Takes a sympy `Array` object (more specifically, `Array` of `Function`) and converts it to a list of lambda functions.

RETURNS - lambda\_list: `list[typing.Callable]` ~~ List of lambda functions to be used for numerical computing.

PARAMETERS:
- coordinates: `geodpy.coordinates.Coordinates` ~~ Coordinates system to be used for the conversion of the array of expressions.
- expressions: `sympy.Array` ~~ Array of functions to convert.
