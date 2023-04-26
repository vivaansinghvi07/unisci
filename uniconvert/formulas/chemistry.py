from sympy import Eq, symbols, solve, log, sqrt
from typing import Union
from uniconvert.types import *
from uniconvert.types import numeric
from uniconvert.error import *
from uniconvert.constants import *
from uniconvert.conversion_factors import *

UNKNOWN = 'x'

def _get_number(value: Union[Quantity, numeric], intended_types: dict, name: str) -> numeric:
    
    # return a symbol if none - represents a variable
    if value is None:
        return symbols(UNKNOWN)
    
    if isinstance(value, (Temperature, Quantity)):

        # standarizes to quantity
        if isinstance(value, Temperature):
            value = Quantity(value.kelvin, {'K': 1})

        # eliminate all special types from intended
        quan_intended_types = Quantity(1, intended_types.copy())
        quan_intended_types = quan_intended_types.to_base_units()
        value = value.converted(list(intended_types.keys())).to_base_units()

        # fully match value with intended types - turn off auto format for this
        old_format = Quantity.auto_format
        Quantity.set_auto_format(False)
        value = value.converted(list(quan_intended_types.unit_type.keys()))
        Quantity.set_auto_format(old_format)
        
        if value.units != quan_intended_types.units:
            raise CompatabilityError(f"The units of '{name}' are not compatible with the equation.")
        
        # returns the converted value number
        return value.value
    
    # normal number passes check
    elif isinstance(value, (float, int)):
        return value
    
    else:
        raise UnsupportedError(f"Unsupported datatype given for '{name}'.")
    
def _get_args(types: dict[str, dict[str, int]], arguments: dict[str, Union[Quantity, numeric]]) -> dict[str, numeric]:
    """
    Arguments: two dictionaries, one of types of each of the arguments in the other. Keys should match.

    Raises: ArgumentError for if the arguments dictionary is not missing one value

    Returns: a new dictionary with numerical values
    """

    # checks arguments were rights
    if list(arguments.values()).count(None) != 1:
        raise ArgumentError("You must have exactly one missing argument.")
    
    # asserts types are valid and converts to numbers
    args = {name: _get_number(value=var, intended_types=types[name], name=name) for name, var in arguments.items()}
    return args

def nernst_equation(reduction_potential: Union[numeric, Quantity] = None,
                    standard_potential: Union[numeric, Quantity] = None,
                    temperature: Union[numeric, Temperature, Quantity] = None,
                    reaction_quotient: numeric = None,
                    electron_count: numeric = None) -> Quantity:
    """
    Arguments: Four out of the following five: 
    - reduction_potential (V)
    - standard_potential (V)
    - temperature (K)
    - reaction_quotient
    - electron_count

    Raises: ArgumentError for too many or too little known values.

    Returns: The missing value in the Nernst Equation
    """

    # convert to dict with name
    arguments = {
        "reduction_potential": reduction_potential,
        "standard_potential": standard_potential,
        "temperature": temperature,
        "reaction_quotient": reaction_quotient,
        "electron_count": electron_count
    }

    # supported units for each things 
    types = {
        "reduction_potential": {'V': 1},
        "standard_potential": {'V': 1},
        "temperature": {'K': 1},
        "reaction_quotient": {},
        "electron_count": {}
    }

    args = _get_args(types=types, arguments=arguments)

    equation = Eq(args["standard_potential"] - 
                (R_JOUL.value * args["temperature"] / (args["electron_count"] * F.value))
                * log(args["reaction_quotient"]), args["reduction_potential"])
    
    solution = solve(equation, (symbols(UNKNOWN)))
    
    return solution[0]

def buffer_system(K_a: Union[numeric, Quantity] = None,
                 acid_concentration: Union[numeric, Quantity] = None,
                 base_concentration: Union[numeric, Quantity] = None,
                 pH: numeric = None):
    """
    Note: This function assumes dissassociation into one proton only.
    Arguments: four of the following, interpreted to the following units: 
    - K_a
    - pH
    - acid_concentration (M)
    - base_concentration (M)

    Raises: ArgumentError for wrong argument count. One must be empty. A CompatabilityError for incompatible values.

    Returns: the missing value as a number.
    """

    arguments = {
        "ka": K_a,
        "initial_conc_acid": acid_concentration,
        "initial_conc_base": base_concentration,
        "pH": pH
    }

    types = {
        "ka": {},
        "initial_conc_acid": {'M': 1},
        "initial_conc_base": {'M': 1},
        "pH": {}
    }

    args = _get_args(types=types, arguments=arguments)

    equation = Eq(args["pH"], -log(args["ka"], 10) + log(args["initial_conc_base"] / args["initial_conc_acid"], 10))

    solution = solve(equation, (symbols(UNKNOWN)))

    return solution[0]

def weak_acid(K_a: Union[numeric, Quantity] = None,
              acid_concentration: Union[numeric, Quantity] = None,
              pH: numeric = None):
    """
    Note: This function assumes dissassociation into one proton only.
    Arguments: two of the following, in the following units:
    - K_a
    - pH
    - acid_concentration (M)

    Raises: ArgumentError for wrong argument count. One must be empty. A CompatabilityError for incompatible values.

    Returns: the missing value as a number.
    """

    arguments = {
        "ka": K_a,
        "initial_conc": acid_concentration,
        "pH": pH
    }

    types = {
        "ka": {},
        "initial_conc": {'M': 1},
        "pH": {}
    }

    args = _get_args(types=types, arguments=arguments)

    equation = Eq(args['ka'], ((10**(-args['pH']))**2/(args['initial_conc'] - 10**(-args['pH']))))

    solution = solve(equation, (symbols(UNKNOWN)))

    return solution[0]

def weak_base(K_b: Union[numeric, Quantity] = None,
                 base_concentration: Union[numeric, Quantity] = None,
                 pH: numeric = None):
    """
    Note: This function assumes dissassociation into one proton only, and no initial concentrations of anything else.
    Arguments: two of the following, in the given units: 
    - K_b
    - pH
    - base_concentration (M)

    Raises: ArgumentError for wrong argument count. One must be empty. A CompatabilityError for incompatible values.

    Returns: the missing value as a number.
    """

    arguments = {
        "kb": K_b,
        "initial_conc": base_concentration,
        "pH": pH
    }

    types = {
        "kb": {},
        "initial_conc": {'M': 1},
        "pH": {}
    }

    args = _get_args(types=types, arguments=arguments)

    equation = Eq(args['kb'], ((10**(-(14-args['pH'])))**2/(args['initial_conc'] - 10**(-(14-args['pH'])))))

    solution = solve(equation, (symbols(UNKNOWN)))

    return solution[0]

def ideal_gas(pressure: Union[numeric, Quantity] = None,
              volume: Union[numeric, Quantity] = None,
              moles: Union[numeric, Quantity] = None,
              temperature: Union[numeric, Temperature, Quantity] = None) -> numeric:
    """
    Arguments: Enter three of the following four:
    - pressure (atm)
    - volume (L)
    - moles (mol)
    - temperature (K)

    Raises: ArgumentError for wrong argument count. One must be empty. A CompatabilityError for incompatible values.

    Returns: the missing value as a number.
    """

    arguments = {
        "pressure": pressure,
        "volume": volume,
        "moles": moles,
        "temperature": temperature
    }

    types = {
        "pressure": {'atm': 1},
        "volume": {'L': 1},
        "moles": {'mol': 1},
        "temperature": {'K': 1}
    }

    args = _get_args(types=types, arguments=arguments)

    # PV = nRT
    equation = Eq(args['pressure'] * args['volume'], args['moles'] * R_ATM.value * args['temperature'])

    solutions = solve(equation, (symbols(UNKNOWN)))

    return solutions[0]
    