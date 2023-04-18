from unit import Quantity
from error import QuantityError
from constants import *

def convert_length(unit: Quantity, target: str, original: str = None) -> Quantity:

    """
    Arguments: a Quantity object, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a QuantityError if the unit entered is not supported.

    Returns: a new Quantity object, with the original unit converted to the target unit. 
    """

    CONVERT_TO_METERS = {
        'ft': 0.3048, 'yd': 0.9144, 'in': 0.0254, 'mi': 1609, 'ly': 946 * 10**13,
        'au': 1496 * 10**8, 'pc': 31 * 10**15, 'm': 1, 'nm': 10**(-9), 'mcm': 10**(-6),
        'mm': 10**(-3), 'cm': 10**(-2), 'km': 10**3, 'Mm': 10**6, 'Gm': 10**9
    }
    
    CONVERT_FROM_METERS = {key: 1 / value for key, value in CONVERT_TO_METERS.items()}

    # checks for illegal values
    if (target not in CONVERT_TO_METERS):
        raise QuantityError("Target unit is not supported in this function.")
    elif original != None and original not in CONVERT_TO_METERS:
        raise QuantityError("Original unit is not supported in this function.")
    
    # auto-determines and converts every source unit
    conversion_factor = 1
    new_units = {target: 0}
    for type in unit.unit_type: 
        if (original == None and type in CONVERT_TO_METERS) or (original != None and type == original):
            conversion_factor *= (CONVERT_TO_METERS[type] * CONVERT_FROM_METERS[target]) ** unit.unit_type[type]
            new_units[target] += unit.unit_type[type]
        else:
            new_units[type] = unit.unit_type[type]

    # returns a new unit with the conversion applied
    return Quantity(conversion_factor * unit.number, new_units)

    


