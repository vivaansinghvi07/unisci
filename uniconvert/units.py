from __future__ import annotations
from typing import Union
from .error import UnitError
from .conversion_factors import *

class Quantity:

    _EXP_CHARS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    _NEG_EXP = "⁻"

    precision = 3

    def set_precision(decimal_places: int):

        """
        Sets the precision of quantity printing. A precision of '3' means 123456 would be printed as 1.234*10⁵
        """

        Quantity.precision = decimal_places

    def __init__(self, number: Union[int, float], unit_type: dict):
        """
        Arguments: Enter the number of the measurement, and a dictionary in the form of {unit: power}. For example, 10 m/s becomes Quantity(10, {'m': 1, 's': -1})

        Creates a new Quantity object using a number and its corresponding unit.
        """

        # makes sure number is valid
        try:
            self.number = float(number)
        except: 
            raise ValueError("Number could not be converted to float.")
        
        # assigns unit settings, each key is in lowercase
        self.unit_type = {key: value for key, value in unit_type.items()}
        self._rm_zeroes()
        
    def __str__(self) -> str:

        """
        Returns the unit as if it was written. Ex: '100.0 m' or '120 ft/s'
        """

        # formats and returns string
        self._rm_zeroes()
        units = "-".join([Quantity._format_unit(unit, power) for unit, power in self.unit_type.items()])
        return f"{Quantity._format_num(self.number)} {units}"
    
    def __repr__(self) -> str:
        
        """
        Returns: how the unit would be constructed.
        """
        return f"Quantity({self.number}, {self.unit_type})"
    
    def __copy__(self) -> Quantity:
        
        """
        Returns: a new copy of the Quantity without changing the dictionary
        """

        return Quantity(self.number, self.unit_type.copy())
    
    def __mul__(self, other: Union[Temperature, Quantity, int, float]) -> Quantity:
        """
        Arguments: A Quantity, Temperature, or number to which you want to multiply the quantity

        Raises: UnsupportedError, for a class that is not supported in multiplication

        Returns: A new Quantity with multiplied units and numbers
        """

        # copies unit types for returning
        new_types = self.unit_type.copy()

        # checks if its a number
        if isinstance(other, int) or isinstance(other, float):
            return Quantity(self.number * other, new_types)
        elif isinstance(other, Temperature):
            if other.type in new_types:
                new_types[other.type] += 1
            else:
                new_types[other.type] = 1
            return Quantity(self.number * other.number, new_types)
        elif isinstance(other, Quantity):
            for type, power in other.unit_type.items():
                if type not in new_types:
                    new_types[type] = power
                else:
                    new_types[type] += power
            return Quantity(self.number * other.number, new_types)
        else:
            raise TypeError("Invalid type for Quantity multiplication.")

    def _rm_zeroes(self):
        
        """
        Removes all units that are to the power of 0.
        """

        for key in self.unit_type:
            if self.unit_type[key] == 0:
                del self.unit_type[key]


    def _format_num(num: Union[int, float]):

        # formats number and gets exponent
        rounded_num = format(num, f".{Quantity.precision}e")
        number, exp = rounded_num.split("e")

        # fills exponent string
        exp_string = "10"
        exp_number_string = ""
        for digit in exp:
            if digit == "+":
                continue
            elif digit == "-":
                exp_string += Quantity._NEG_EXP
            else:
                exp_number_string += Quantity._EXP_CHARS[int(digit)]
        
        # remove leading zeroes
        exp_number_string = exp_number_string.lstrip(Quantity._EXP_CHARS[0])
        exp_string += exp_number_string

        # returns formatted number
        return f"{number}*{exp_string}"

    def _format_unit(unit: str, power: int) -> str:
        """
        Arguments: An integer power to raise the number to

        Returns: A string that contains the unit raised the power
        """

        # start output with the unit
        output = unit

        # check if its just one
        if power == 1:
            return output
    
        # control negatives
        elif power < 0:
            output += Quantity._NEG_EXP
            power = abs(power)

        # adds the digits
        for digit in str(power):
            output += Quantity._EXP_CHARS[int(digit)]

        # adds degree symbol for temperature unit
        if unit.upper() in ['F', 'C']:
            output = Temperature.DEG_SYMB + output

        return output
    
    def converted_auto(self, target_units: list) -> Quantity:

        """
        Arguments: A list of units to convert to. The program will try to convert the Quantity to each unit provided in this list.

        Raises: UnitError for unsupported units.
        
        Returns: a new Quantity object with possible unit converted to the other_conversions, if possible.
        """

        output = self.__copy__()

        for conversion in target_units:
            if conversion in LENGTH_UNITS:
                output = output.converted_length(conversion)
            elif conversion in MASS_UNITS:
                output = output.converted_mass(conversion)
            elif conversion in TIME_UNITS:
                output = output.converted_time(conversion)
            else:
                raise UnitError(f"Unsupported unit provided: '{conversion}'.")

        return output

    def _converted(self, factors: dict, target: str, original: str = None) -> Quantity:

        """
        Arguments: a dictionary of conversion factors in this format: {'units': LIST1, 'to': DICT1, 'from': DICT2}, 
        where units are the supported units for the conversion. Also takes in the target unit and original unit. 
        If original is not entered, it is automatically interpreted.
        
        Returns: a new Quantity with the conversion being done on it
        """

        # loads dictionaries
        supported = factors['units']
        to_dict = factors['to']
        from_dict = factors['from']

        # checks for illegal values
        if (target not in supported):
            raise UnitError("Target unit is not supported in this function.")
        elif original != None and original not in supported:
            raise UnitError("Original unit is not supported in this function.")
        
        # auto-determines and converts every source unit
        conversion_factor = 1
        new_units = {target: 0}
        for type in self.unit_type: 
            if (original == None and type in supported) or (original != None and type == original):
                conversion_factor *= (to_dict[type] * from_dict[target]) ** self.unit_type[type]
                new_units[target] += self.unit_type[type]
            else:
                new_units[type] = self.unit_type[type]

        # returns a new unit with the conversion applied
        return Quantity(conversion_factor * self.number, new_units)

    def converted_length(self, target: str, original: str = None) -> Quantity:

        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self._converted(factors={
            'units': LENGTH_UNITS,
            'to': CONVERT_TO_METERS,
            'from': CONVERT_FROM_METERS
        }, target=target, original=original)
    
    def converted_mass(self, target: str, original: str = None) -> Quantity:
        
        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self._converted(factors={
            'units': MASS_UNITS,
            'to': CONVERT_TO_KILOGRAMS,
            'from': CONVERT_FROM_KILOGRAMS
        }, target=target, original=original)

    def converted_time(self, target: str, original: str = None) -> Quantity:
        
        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self._converted(factors={
            'units': TIME_UNITS,
            'to': CONVERT_TO_SECONDS,
            'from': CONVERT_FROM_SECONDS
        }, target=target, original=original)

class Temperature:

    DEG_SYMB = "°"

    def __init__(self, number: Union[int, float], type: str):

        """
        Arguments: Number (number for the temperature), type of the temperature (enter 'C', 'K', or 'F')
        Quantity objects can have temperature units, but they cannot be converted. Temperature objects can be.

        Raises: UnitError if there is a wrong unit of measurement
        """

        if type.upper() not in ['C', 'K', 'F']:
            raise UnitError(f"Invalid unit of measurement for a temperature: '{type}'")

        self.type = type.upper()
        self.number = number

    def __str__(self):
        """
        Returns the temperature in the form <number> <symbol>. For example, '100 K' or '50°F'
        """
        symbol = Temperature.DEG_SYMB if self.type != 'K' else ' '
        return f"{self.number}{symbol}{self.type}"

    @property
    def celsius(self):
        """
        Returns the temperature in degrees Celsius
        """
        if self.type == 'C':
            return self.number
        elif self.type == 'F':
            return (self.number - 32) * 5 / 9
        elif self.type == 'K':
            return self.number - 273
        
    @property
    def fahrenheit(self):
        """
        Returns the temperature in degrees Fahrenheit
        """
        if self.type == 'F':
            return self.number
        elif self.type == 'C':
            return self.number * (9 / 5) + 32
        elif self.type == 'K':
            return (self.number + 273) * (9 / 5) + 32
        
    @property
    def kelvin(self):
        """
        Returns the temperature in Kelvin
        """ 
        if self.type == 'K':
            return self.number
        elif self.type == 'C':
            return self.number + 273
        elif self.type == 'F':
            return (self.number - 32) * (5 / 9) + 273
    
    def convert(self, target: str):
        """
        Arguments: A single character representing the unit of the target temperature (eg 'K' or 'F')

        Raises: UnitError for a wrong temperature unit
        """

        # standardize to uppercase
        target = target.upper()

        # check for invalid
        if target not in ['F', 'C', 'K']:
            raise UnitError(f"Target unit '{target}' is not a supported temperature.")
        
        # perform number conversion
        if target == 'K':
            self.number = self.kelvin
        elif target == 'C':
            self.number = self.celsius
        elif target == 'F':
            self.number = self.fahrenheit

        # update type
        self.type == target

