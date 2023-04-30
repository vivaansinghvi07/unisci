from sympy import symbols
from unisci.error import *
from unisci.types import *
from unisci.types import numeric
from typing import Union

UNKNOWN = 'x'

def __get_number(value: Union[Quantity, numeric], intended_types: dict, name: str) -> numeric:
    
    # return a symbol if none - represents a variable
    if value is None:
        return symbols(UNKNOWN)
    
    if isinstance(value, (Temperature, Quantity)):

        # standarizes to quantity
        if isinstance(value, Temperature):
            value = Quantity(value.kelvin, {'K': 1})

        # eliminate all special types from intended
        quan_intended_types = Quantity(1, intended_types.copy())
        quan_intended_types = quan_intended_types.to_base_units()
        value = value.converted(list(intended_types.keys())).to_base_units()

        # fully match value with intended types - turn off auto format for this
        old_format = Quantity.auto_format
        Quantity.set_auto_format(False)
        value = value.converted(list(quan_intended_types.unit_type.keys()))
        Quantity.set_auto_format(old_format)
        
        if value.units != quan_intended_types.units:
            raise CompatabilityError(f"The units of '{name}' are not compatible with the equation.")
        
        # returns the converted value number
        return value.value
    
    # normal number passes check
    elif isinstance(value, (float, int)):
        return value
    
    else:
        raise UnsupportedError(f"Unsupported datatype given for '{name}'.")
    
def _get_args(types: dict[str, dict[str, int]], arguments: dict[str, Union[Quantity, numeric]]) -> dict[str, numeric]:
    """
    Arguments: two dictionaries, one of types of each of the arguments in the other. Keys should match.

    Raises: ArgumentError for if the arguments dictionary is not missing one value

    Returns: a new dictionary with numerical values
    """

    # checks arguments were rights
    if list(arguments.values()).count(None) != 1:
        raise ArgumentError("You must have exactly one missing argument.")
    
    # asserts types are valid and converts to numbers
    args = {name: __get_number(value=var, intended_types=types[name], name=name) for name, var in arguments.items()}
    return args