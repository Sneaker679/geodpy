# expr\_to\_lambda()
DESCRIPTION: Takes a sympy `Function` object and converts it to a lambda function. This is not meant to be used outside this project's, as it assumes many things.

RETURNS - lambda: typing.Callable ~~ Lambda function to be used for numerical solving.

PARAMETERS:
- coordinates: `geodpy.Coordinates` ~~ Coordinates system to be used for the conversion of the expression.
- expression: `sympy.Function` ~~ Expression to be converted.

