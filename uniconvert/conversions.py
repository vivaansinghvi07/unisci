from uniconvert.error import UnitError
from uniconvert.constants import *
from uniconvert.conversion_factors import *
from typing import Union

__all__ = [
    'convert_length',
    'convert_mass',
    'convert_time',
    'convert_volume',
    'convert'
]

def _check_illegal(target: str, original: str, units: dict):

    """
    Makes sure that the target and original units are supported for each other
    """

    # checks for illegal values
    if target not in units:
        raise UnitError(f"Target unit '{target} 'is not supported in this function.")
    elif original not in units:
        raise UnitError(f"Original unit '{original} is not supported in this function.")    


def convert_length(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports length conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    _check_illegal(target, original, LENGTH_UNITS)
    
    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_METERS[original] * CONVERT_FROM_METERS[target]
    return number * conversion_factor
    
def convert_mass(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports mass conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    _check_illegal(target, original, MASS_UNITS)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_KILOGRAMS[original] * CONVERT_FROM_KILOGRAMS[target]
    return number * conversion_factor

def convert_time(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports time conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    _check_illegal(target, original, TIME_UNITS)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_SECONDS[original] * CONVERT_FROM_SECONDS[target]
    return number * conversion_factor

def convert_volume(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports volume conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    _check_illegal(target, original, VOLUME_UNITS)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_LITERS[original] * CONVERT_FROM_LITERS[target]
    return number * conversion_factor

def convert(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    General-purpose converson between units, as opposed to specific conversions like convert_mass() or convert_time()

    Arguments: a number, and original unit, and a target unit.

    Raises: a Unit Error if the units do not match type.

    Returns: a new number with the original unit converted to the target unit.
    """

    conversion_functions = [convert_length, convert_mass, convert_time, convert_volume]
    for func in conversion_functions:
        try:
            return func(number, target, original)
        except:
            continue

    # raises error if no function succeeded
    raise UnitError("Target or original units are incompatiple or unsupported.")

def conversion_factor(target: str, original: str) -> Union[int, float]:

    """
    Returns the conversion factor (what you need to multiply the original unit by) between two units

    Arguments: Two units - an original and a target.
    
    Raises: a UnitError for incompatible units.
    """

    # gets ocnversion factor by converting the number 1
    return convert(1, target, original)