from unisci._error import *
from unisci._conversion_factors import *
from typing import Union

# what you need to multiply each of these by to get the base metric
METRIC_CONVERSIONS = {
    'y': 1e-24,
    'z': 1e-21,
    'a': 1e-18,
    'f': 1e-15,
    'p': 1e-12,
    'n': 1e-9,
    'µ': 1e-6,
    'mc': 1e-6,     # for those who cannot use the µ symbol
    'u': 1e-6,      # alternate option
    'm': 1e-3,
    'c': 1e-2,
    'd': 1e-1,
    'da': 1e1,
    'h': 1e2,
    'k': 1e3,
    'M': 1e6,
    'G': 1e9,
    'T': 1e12,
    'P': 1e15,
    'E': 1e18,
    'Z': 1e21,
    'Y': 1e24
}
METRIC_UNITS = ['s', 'm', 'g', 'K', 'mol', 'J', 'W', 'N', 'Pa', 'L']     # the ones that are currently supported

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