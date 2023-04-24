from uniconvert.types import *
from uniconvert.conversions import *

def find_delta_velocity(time: Quantity) -> Quantity:

    """
    Example of multiplication involving Quantities:

    >>> seconds = Quantity(1.5, {'s': 1})
    >>> print(find_delta_velocity(time=seconds))
    '-1.470*10¹ m/s'
    """
    
    g = Quantity(-9.8, {'m': 1, 's': -2})
    return time * g

def find_force(m: Quantity, a: Quantity) -> Quantity:
    """
    Example of auto-conversion for Quantities:

    >>> a = Quantity(9.8, {'m': 1, 's': -2})
    >>> m = Quantity(10, {'kg': 1})
    >>> print(find_force(m=m, a=a))
    '9.800*10¹ N'
    >>> Quantity.set_auto_format(False)
    >>> print(find_force(m=m, a=a))
    '9.800*10¹ kg-m/s²'
    """

    return((m * a).standardized_physics())


a = Quantity(1, {'mmol': 1, 'g': -1})
print(a)
b = a.converted_auto(['mol'])
print(b)
c = b.converted_mass('mg')
print(c)