from typing import Union
from error import UnitError

class Quantity:

    _EXP_CHARS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    _NEG_EXP = "⁻"
    
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
        
    def __str__(self):

        """
        Returns the unit as if it was written. Ex: '100.0 m' or '120 ft/s'
        """

        # formats and returns string
        self._rm_zeroes()
        units = "-".join([Quantity._get_exp(unit, power) for unit, power in self.unit_type.items()])
        return f"{self.number} {units}"
    
    def __repr__(self):
        
        """
        Returns how the unit would be constructed.
        """
        pass

    def _rm_zeroes(self):
        
        """
        Removes all units that are to the power of 0.
        """

        for key in self.unit_type:
            if self.unit_type[key] == 0:
                del self.unit_type[key]

    def _get_exp(unit: str, power: int) -> str:
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
    
    def round(self, digs: int):

        """
        Rounds the number of the Quantity object to a certain number of digits.

        Helpful if you want to print it with rounding.
        """

        self.number = round(self.number, digs)

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