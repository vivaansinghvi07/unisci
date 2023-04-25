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
METRIC_UNITS = ['s', 'm', 'g', 'K', 'mol', 'J', 'W', 'N']     # the ones that are currently supported

# for length: convert between the units shown here
CONVERT_TO_METERS = {
    'ft': 0.3048, 
    'yd': 0.9144, 
    'in': 0.0254, 
    'mi': 1609, 
    'ly': 946e13,
    'au': 1496e8, 
    'pc': 31e15, 
    'm': 1
}

# for mass conversions
CONVERT_TO_GRAMS = {
    'g': 1,
    'lb': 454,
    'oz': 454 / 16,
    'st': 6356,
    'amu': 1.661e-24
}

# for time conversions
CONVERT_TO_SECONDS = {
    's': 1,
    'min': 60,
    'hr': 3600,
    'day': 3600 * 24,
    'wk': 3600 * 24 * 7,
    'yr': 3600 * 24 * 7 * 365.25
}

# for volume conversions
CONVERT_TO_LITERS = {
    'L': 1,
    'c.': 0.2366,
    'pt.': 0.2366 * 2,
    'qt.': 0.2366 * 4,
    'gal.': 0.2366 * 16,
    'fl. oz': 0.2366 / 8,
    'tbsp': 0.2366 / 16,
    'tsp': 0.2366 / 48
}

# for temperature converisons (absolute, not relative)
CONVERT_TO_KELVIN = {
    'deg. C': 1,
    'deg. F': 5 / 9,
    'K': 1,
}

# supported units for auto-simplification - first one for each special unit must be in the most basic form
AUTO_SIMPLIFY = [
    [{'kg': 1, 'm': 1, 's': -2}, 'N'],      # Newtons
    [{'J': 1, 'm': -1}, 'N'],
    [{'kg': 1, 'm': 2, 's': -2}, 'J'],      # Joules
    [{'N': 1, 'm': 1}, 'J'],             
    [{'kg': 1, 'm': 2, 's': -3}, 'W'],      # Watts
    [{'N': 1, 'm': 1, 's': -1}, 'W'],
    [{'J': 1, 's': -1}, 'W'],          
    [{'mol': 1, 'L': -1}, 'M'],             # Molarity
    [{'dm': 3}, 'L'],                       # Liters
    [{'cm': 3}, 'mL'],                      # Milliliters
    [{'J': 1, 'C': -1}, 'V']                # Volts
]
FORCE_SIMPLIFY = {
    'N': {'kg': 1, 'm': 1, 's': -2},        # Newtons
    'J': {'kg': 1, 'm': 2, 's': -2},        # Joules
    'W': {'kg': 1, 'm': 2, 's': -3},        # Watts
    'L': {'dm': 3},                         # Liters
    'mL': {'cm': 3},                        # Milliliters
    'M': {'mol': 1, 'L': -1},               # Molarity
}
SPECIAL_UNITS = set([unit for _, unit in AUTO_SIMPLIFY])    # stores the special units (['N', 'J', ...])
FORCED_SPECIAL_UNITS = list(FORCE_SIMPLIFY.keys())