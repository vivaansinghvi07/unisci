from typing import Union

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

        return output
    
    def round(self, digs: int):

        """
        Rounds the number of the Quantity object to a certain number of digits.

        Helpful if you want to print it with rounding.
        """

        self.number = round(self.number, digs)

    def _standardize(self):
        pass

class Temperature:
    pass