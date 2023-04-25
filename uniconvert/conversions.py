from uniconvert.error import *
from uniconvert.conversion_factors import *
from typing import Union

__all__ = [
    'convert_length',
    'convert_mass',
    'convert_time',
    'convert_volume',
    'convert',
    'metric_base',
    'metric_factor',
    'conversion_factor',
    'convert_metric',
]

def _check_illegal(target: str, original: str, units: list):

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

    supported = list(CONVERT_TO_METERS.keys())

    _check_illegal(target, original, supported)
    
    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_METERS[original] / CONVERT_TO_METERS[target]
    return number * conversion_factor
    
def convert_mass(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports mass conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    supported = list(CONVERT_TO_GRAMS.keys())

    _check_illegal(target, original, supported)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_GRAMS[original] / CONVERT_TO_GRAMS[target]
    return number * conversion_factor

def convert_time(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports time conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    supported = list(CONVERT_TO_SECONDS.keys())

    _check_illegal(target, original, supported)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_SECONDS[original] / CONVERT_TO_SECONDS[target]
    return number * conversion_factor

def convert_volume(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    Note: For complicated conversions, it is better to use Quantity objects. This method only supports volume conversions.

    Arguments: a number, an original unit and a target unit. If original is not entered, it is automatically interpreted.

    Raises: a UnitError if the unit entered is not supported.

    Returns: a new number with the original unit converted to the target unit. 
    """

    supported = list(CONVERT_TO_LITERS.keys())

    _check_illegal(target, original, supported)

    # calculate conversion factor and convert
    conversion_factor = CONVERT_TO_LITERS[original] / CONVERT_TO_LITERS[target]
    return number * conversion_factor

def convert(number: Union[int, float], target: str, original: str) -> Union[int, float]:

    """
    General-purpose converson between units, as opposed to specific conversions like convert_mass() or convert_time()

    Arguments: a number, and original unit, and a target unit.

    Raises: a Unit Error if the units do not match type.

    Returns: a new number with the original unit converted to the target unit.
    """

    conversion_functions = [convert_length, convert_mass, convert_time, convert_volume, convert_metric]
    for func in conversion_functions:
        try:
            return func(number, target, original)
        except:
            continue

    # raises error if no function succeeded
    raise UnitError("Target or original units are incompatiple or unsupported.")

def metric_base(unit: str) -> str:
    """
    Returns the base metric SI unit of the unit. If the unit is not metric, returns the unit itself.
    """
    for base in METRIC_UNITS:
        # try-except block for if the tested base is longer than the unit
        try:
            test_base = unit[-len(base):]
            if test_base == base:
                if unit[:-len(base)] in METRIC_CONVERSIONS:
                    return test_base
                else:
                    return unit     # options: 1) base is taken and incorrect, 2) base is already at base form
            else:
                continue    # checks another base
        except: 
            continue

    # if no base matches (most likely option)
    return unit
    

def metric_factor(unit: str) -> Union[int, float]:
    """
    Returns the number to multiply by the unit in order to get a base in the metric system. 
    Returns 1 if the number is not metric.
    """
    # get base and check that it is different
    base = metric_base(unit)
    if base == unit:
        return 1
    
    # otherwise return the conversion factor
    else:
        return METRIC_CONVERSIONS[unit[:-len(base)]]
    
def convert_metric(number: Union[int, float], original: str, target: str) -> Union[int, float]:
    """
    Arguments: a number, an original unit, and a target unit. The original and target units must have the same base metric.

    Raises: UnsupportedError for if units not in the METRIC_UNITS constant. CompatabilityError for uncompatible units.

    Returns: the new converted number.
    """

    # make sure base is the same
    if metric_base(target) not in METRIC_UNITS or metric_base(original) not in METRIC_UNITS:
        raise UnsupportedError("Units not supported for metric conversions.")
    elif metric_base(target) != metric_base(original):
        raise CompatabilityError("Metric base form must match for conversions.")
    
    # returns converted number if all good
    return metric_factor(original) / metric_factor(target) * number

def conversion_factor(target: str, original: str) -> Union[int, float]:

    """
    Returns the conversion factor (what you need to multiply the original unit by) between two units

    Arguments: Two units - an original and a target.
    
    Raises: a UnitError for incompatible units.
    """

    # gets ocnversion factor by converting the number 1
    return convert(1, target, original)