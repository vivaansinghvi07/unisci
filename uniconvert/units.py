from __future__ import annotations
from typing import Union
from uniconvert.error import UnitError
from uniconvert.conversion_factors import *

class Quantity:

    _EXP_CHARS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    _NEG_EXP = "⁻"

    precision = 3
    auto_format = True

    def set_precision(decimal_places: int):

        """
        Sets the precision of quantity printing. 
        
        A precision of '3' means 123456 would be printed as 1.234*10⁵
        """

        Quantity.precision = decimal_places

    def auto_format(do: bool):
        """
        Sets instruction for values to auto-format, taking in a boolean for if it should or not.
        For example, if a Quantity has units 'in' and 'm', auto format automatically converts it to either in² or m²
        """

        Quantity.auto_format = do

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
        self.__rm_zeroes()
        
    def __str__(self) -> str:

        """
        Returns the unit as if it was written. Ex: '100.0 m' or '120 ft/s'
        """

        # formats and returns string
        self.__rm_zeroes()

        # filter positives and negatives
        pos, neg = {}, {}
        for key, value in self.unit_type.items():
            if value < 0:
                neg[key] = abs(value)
            else:
                pos[key] = value

        # gets positive and negative values
        pos_units = "-".join([Quantity.__format_unit(unit, power) for unit, power in pos.items()])
        neg_units = "-".join([Quantity.__format_unit(unit, power) for unit, power in neg.items()])

        # creates and returns string for units
        if len(pos_units) == 0:
            units = f"1/{neg_units}"
        elif len(neg_units) == 0:
            units = f"{pos_units}"
        else:
            units = f"{pos_units}/{neg_units}"
        return f"{Quantity.__format_num(self.number)} {units}"
    
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
        if isinstance(other, (int, float)):
            return Quantity(self.number * other, new_types)
        
        # checks if it is a temperature unit
        elif isinstance(other, Temperature):
            if other.type in new_types:
                new_types[other.type] += 1
            else:
                new_types[other.type] = 1
            return Quantity(self.number * other.number, new_types)
        
        # checks if it is a Quantity - account for every unit type in new Quantity
        elif isinstance(other, Quantity):
            for type, power in other.unit_type.items():
                if type not in new_types:
                    new_types[type] = power
                else:
                    new_types[type] += power
            answer = Quantity(self.number * other.number, new_types)
        
        # other types unsupported
        else:
            raise TypeError("Invalid type for Quantity multiplication.")
        
        # converts all units if necessary
        if Quantity.auto_format:
            return answer.converted_auto(list(self.unit_type.keys()))
        else:
            return answer
        
    def __rmul__(self, other: Union[Temperature, Quantity, int, float]) -> Quantity:
        """
        Same as multiplication, but in reverse. 
        See documentation of __mul__() for more info about multiplication.
        """
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[Temperature, Quantity, int, float]) -> Quantity:
        """
        Arguments: a Temperature, Quantity, or number to divide the Quantity by.

        Raises: a UnitError for unsupported units

        Returns: a new Quantity object with the division being done.
        """

        new_types = self.unit_type.copy()

        if isinstance(other, (int, float)):

            # divides number and returns
            return Quantity(self.number / other, new_types)

        elif isinstance(other, Temperature):

            # adds the inverse of the temperature
            if other.type in new_types:
                new_types[other.type] = -1
            else:
                new_types[other.type] -= 1

            # returns new Quantity with inverted temperature unit
            return Quantity(self.number / other.number, new_types)

        elif isinstance(other, Quantity):

            # reverses dictionary
            new_types = {unit: - power for unit, power in other.unit_type.items()}
            new_num = 1 / other.number

            # performs multiplication with inverted object
            return self * Quantity(new_num, new_types)
    
    def __rtruediv__(self, other: Union[int, float, Temperature, Quantity]):

        """
        Arguments: a Temperature, Quantity, or number to divide by the Quantity.

        Raises: a UnitError for unsupported units

        Returns: a new Quantity object with the division being done.
        """

        # reverses self dictionary
        new_types = {unit: - power for unit, power in self.unit_type.items()}
    
        if isinstance(other, (int, float)):
            return Quantity(other / self.number, new_types)
        
        elif isinstance(other, (Temperature, Quantity)):
            new_number = 1 / self.number
            return Quantity(new_number, new_types) * other
        
    def __pow__(self, power: int) -> Quantity:

        """
        Raises a Quantity to the power of an integer.
        """

        if not isinstance(power, int):
            raise TypeError("Can only raise to the power of an integer.")

        # performs <power> self multiplications
        output = self.__copy__()
        for _ in range(1, power):
            output = output * self

        return output

    def __rm_zeroes(self):
        
        """
        Removes all units that are to the power of 0.
        """

        for key in self.unit_type.keys():
            if self.unit_type[key] == 0:
                del self.unit_type[key]

    def __format_num(num: Union[int, float]) -> str:

        """
        Formats the number of a Quantity for printing.
        
        For example, 123456 with a precision of 2 becomes 1.23*10⁵
        """

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

        # check if it was 0 to begin with 
        if len(exp_number_string) == 0:
            exp_number_string = Quantity._EXP_CHARS[0]
        
        # appends exponent
        exp_string += exp_number_string

        # returns formatted number
        return f"{number}*{exp_string}"

    def __format_unit(unit: str, power: int) -> str:
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

        return output

    def __converted(self, factors: dict, target: str, original: str = None) -> Quantity:

        """
        Arguments: a dictionary of conversion factors in this format: {'supported': LIST1, 'to': DICT1, 'from': DICT2}, 
        where units are the supported units for the conversion. Also takes in the target unit and original unit. 
        If original is not entered, it is automatically interpreted.
        
        Returns: a new Quantity with the conversion being done on it
        """

        # loads dictionaries
        supported = factors['supported']
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

        return self.__converted(factors={
            'supported': LENGTH_UNITS,
            'to': CONVERT_TO_METERS,
            'from': CONVERT_FROM_METERS
        }, target=target, original=original)
    
    def converted_mass(self, target: str, original: str = None) -> Quantity:
        
        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self.__converted(factors={
            'supported': MASS_UNITS,
            'to': CONVERT_TO_KILOGRAMS,
            'from': CONVERT_FROM_KILOGRAMS
        }, target=target, original=original)

    def converted_time(self, target: str, original: str = None) -> Quantity:
        
        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self.__converted(factors={
            'supported': TIME_UNITS,
            'to': CONVERT_TO_SECONDS,
            'from': CONVERT_FROM_SECONDS
        }, target=target, original=original)
    
    def converted_volume(self, target: str, original: str = None) -> Quantity:
        
        """
        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self.__converted(factors={
            'supported': VOLUME_UNITS,
            'to': CONVERT_TO_LITERS,
            'from': CONVERT_FROM_LITERS
        }, target=target, original=original)
    
    def standardized(self):

        """
        Converts the Quantity to standard SI units (meters, seconds, kilograms, etc.).

        Returns a new Quantity with converted measurements.
        """

        return self.converted_auto(['kg', 'm', 's'])

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