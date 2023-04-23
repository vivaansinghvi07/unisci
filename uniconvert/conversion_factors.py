# for length: convert between the units shown here
CONVERT_TO_METERS = {
    'ft': 0.3048, 
    'yd': 0.9144, 
    'in': 0.0254, 
    'mi': 1609, 
    'ly': 946e13,
    'au': 1496e8, 
    'pc': 31e15, 
    'm': 1, 
    'nm': 1e-9, 
    'mcm': 1e-6,
    'mm': 1e-3, 
    'cm': 1e-2, 
    'km': 1e3, 
    'Mm': 1e6, 
    'Gm': 1e9
}
CONVERT_FROM_METERS = {key: 1 / value for key, value in CONVERT_TO_METERS.items()}
LENGTH_UNITS = list(CONVERT_FROM_METERS.keys())

# for mass conversions
CONVERT_TO_KILOGRAMS = {
    'Gg': 1e6,
    'Mg': 1e3,
    'kg': 1,
    'g': 1e-3,
    'mg': 1e-6,
    'mcg': 1e-9,
    'ng': 1e-12,
    'lb': 0.454,
    'oz': 0.454 / 16,
    'st': 6.356,
    'amu': 1.661e-27
}
CONVERT_FROM_KILOGRAMS = {key: 1 / value for key, value in CONVERT_TO_KILOGRAMS.items()}
MASS_UNITS = list(CONVERT_FROM_KILOGRAMS.keys())

# for time conversions
CONVERT_TO_SECONDS = {
    'ns': 1e-9,
    'mcs': 1e-6,
    'ms': 1e-3,
    's': 1,
    'min': 60,
    'hr': 3600,
    'day': 3600 * 24,
    'wk': 3600 * 24 * 7,
    'yr': 3600 * 24 * 7 * 365.25
}
CONVERT_FROM_SECONDS = {key: 1 / value for key, value in CONVERT_TO_SECONDS.items()}
TIME_UNITS = list(CONVERT_FROM_SECONDS.keys())

# for volume conversions
CONVERT_TO_LITERS = {
    'nL': 1e-9,
    'mcL': 1e-6,
    'mL': 1e-3,
    'cc': 1e-3,
    'L': 1,
    'kL': 1e3,
    'ML': 1e6,
    'GL': 1e9,
    'c.': 0.2366,
    'pt.': 0.2366 * 2,
    'qt.': 0.2366 * 4,
    'gal.': 0.2366 * 16,
    'fl. oz': 0.2366 / 8,
    'tbsp': 0.2366 / 16,
    'tsp': 0.2366 / 48
}
CONVERT_FROM_LITERS = {key: 1 / value for key, value in CONVERT_TO_LITERS.items()}
VOLUME_UNITS = list(CONVERT_FROM_LITERS.keys())

# for temperature converisons (absolute, not relative)
CONVERT_TO_CELSIUS = {
    'deg. C': 1,
    'deg. F': 5 / 9,
    'K': 1,
}
CONVERT_FROM_CELSIUS = {key: 1 / value for key, value in CONVERT_TO_CELSIUS.items()}
TEMPERATURE_UNITS = list(CONVERT_FROM_CELSIUS.keys())

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
METRIC_SI_UNITS = ['s', 'm', 'g', 'K', 'mol', 'J', 'W', 'N']     # the ones that are currently supported

AUTO_SIMPLIFY = [
    [{'kg': 1, 'm': 1, 's': -2}, 'N'],      # Newtons
    [{'N': 1, 'm': 1}, 'J'],                # Joules
    [{'kg': 1, 'm': 2, 's': -2}, 'J'],   
    [{'J': 1, 's': -1}, 'W'],               # Watts
    [{'N': 1, 'm': 1, 's': -1}, 'W'], 
    [{'kg': 1, 'm': 2, 's': -3}, 'W'],
    [{'mol': 1, 'L': -1}, 'M']              # Molarity
]
SPECIAL_UNITS = [unit for _, unit in AUTO_SIMPLIFY]