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
    'st': 6.356,
    'amu': 1.661e-27,
    'u': 1.661e-27
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