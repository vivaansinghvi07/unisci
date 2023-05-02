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
    'dy': 3600 * 24,
    'wk': 3600 * 24 * 7,
    'yr': 3600 * 24 * 365.25
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

# for pressure conversions
CONVERT_TO_ATM = {
    'atm': 1,
    'torr': 0.0013157,
    'mm Hg': 0.0013157,
    'bar': 0.986923,
    'Pa': 0.0000098,
    'psi': 0.068046
}

SIMPLIFICATION = {
    'N': {'kg': 1, 'm': 1, 's': -2},        # Newtons
    'J': {'kg': 1, 'm': 2, 's': -2},        # Joules
    'W': {'kg': 1, 'm': 2, 's': -3},        # Watts
    'L': {'dm': 3},                         # Liters
    'mL': {'cm': 3},                        # Milliliters
    'M': {'mol': 1, 'L': -1},               # Molarity
    'V': {'J': 1, 'C': -1},                 # Volts
    'Pa': {'N': 1, 'm': -2}                 # Pressure (Pascals)
}