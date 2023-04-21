from uniconvert.units import Quantity, Temperature
from typing import Union

def find_delta_velocity(time: Quantity):

    """
    Example of multiplication involving Quantities:

    >>> seconds = Quantity(1.5, {'s': 1})
    >>> print(find_delta_velocity(time=seconds))
    '-1.470*10¹ m/s'
    """
    
    g = Quantity(-9.8, {'m': 1, 's': -2})
    return time * g

