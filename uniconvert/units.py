from __future__ import annotations
import json
from pathlib import Path
from typing import Union
from uniconvert.error import *
from uniconvert.conversion_factors import *

_CONVERT_FUNCS = []

class Quantity:

    _EXP_CHARS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    _NEG_EXP = "⁻"
    _PHYSICS_UNITS = ['m', 's', 'kg', 'L', 'K']
    _CHEMISTRY_UNITS = ['m', 's', 'g', 'L', 'K']

    precision = 3
    auto_format = True

    def __register_conversion(func):
        _CONVERT_FUNCS.append(func)
        return func

    def set_precision(decimal_places: int):

        """
        Sets the precision of quantity printing. 
        
        A precision of '3' means 123456 would be printed as 1.234*10⁵.
        """

        if not isinstance(decimal_places, int):
            raise TypeError("Precision must be an integer.")

        Quantity.precision = decimal_places

    def set_auto_format(do: bool):
        """
        Sets instruction for values to auto-format, taking in a boolean for if it should or not.
        For example, if a Quantity has units 'in' and 'm', auto format automatically converts it to either in² or m².
        """
        Quantity.auto_format = do

    def __init__(self, number: Union[int, float], unit_type: dict):
        """
        Arguments: Enter the number of the measurement, and a dictionary in the form of {unit: power}. For example, 10 m/s becomes Quantity(10, {'m': 1, 's': -1}).

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
        Returns the unit as if it was written. Ex: '100.0 m' or '120 ft/s'.
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
        if len(self.unit_type) == 0:
            units = ""
        elif len(pos_units) == 0:
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
        Returns: a new copy of the Quantity without changing the dictionary.
        """

        return Quantity(self.number, self.unit_type.copy())
    
    def __add__(self, other: Union[Quantity, int, float]) -> Quantity:

        """
        Arguments: a Quantity, Temperature, or number which you want to add to the Quantity.

        Raises: UnsupportedError, for classes not supported in adding. CompatabilityError, for Quantities not compatible for adding.

        Returns: a new Quantity with the addition operation performed on it.
        """

        self.__rm_zeroes()

        if isinstance(other, (int, float)):

            # makes sure it is unitless
            if not len(self.unit_type) == 0:
                raise CompatabilityError("Quantity must be unitless for addition with number.")
            
            # just performs the addition
            return Quantity(self.number + other, {})

        elif isinstance(other, Temperature):

            raise CompatabilityError("A Quantity (absolute temperature) is incompatible for addition with a Temperature (relative temperature)")
        
        elif isinstance(other, Quantity):

            # automatically convert all the other's units to self's units
            other = other.converted_auto(list(self.unit_type.keys()))

            # check for incompatability
            if len(self.unit_type) != len(other.unit_type):
                raise CompatabilityError("Quantity addition requires units to be of the same type and order.")
            
            # checks that all powers are the same
            for key in self.unit_type.keys():
                try:
                    if other.unit_type[key] != self.unit_type[key]:
                        raise CompatabilityError("Quantity addition requires units to be of the same type and order.")
                except:
                    raise CompatabilityError("Quantity addition requires units to be of the same type and order.")
                
            return Quantity(self.number + other.numbers, self.unit_type.copy())
        
        else:
            raise UnsupportedError("Type is not supported for addition with Quantity.")
        
    def __radd__(self, other: Union[int, float, Quantity]) -> Quantity:

        """
        Performs addition when the Quantity is on the right.
        """

        # performs normal addition
        return self + other
    
    def __sub__(self, other: Union[int, float, Quantity]) -> Quantity:

        """
        Performs subtraction in the form negative addition. See __add__() method for more details.
        """

        return self + (-1 * other)
    
    def __rsub__(self, other: Union[int, float, Quantity]) -> Quantity:

        """
        Subtracts the Quantity from another number or Quantity. See __add__() method for more details.
        """

        return (self * -1) + other
    
    def __mul__(self, other: Union[Quantity, int, float]) -> Quantity:

        """
        Arguments: A Quantity or number to which you want to multiply the quantity.

        Raises: UnsupportedError, for a class that is not supported in multiplication.

        Returns: A new Quantity with multiplied units and numbers.
        """

        # copies unit types for returning
        new_types = self.unit_type.copy()

        # checks if its a number
        if isinstance(other, (int, float)):
            return Quantity(self.number * other, new_types)
        
        # checks if it is a temperature unit
        elif isinstance(other, Temperature):
            
            raise CompatabilityError("A Quantity (absolute temperature) is incompatible for addition with a Temperature (relative temperature)")

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
            raise UnsupportedError("Invalid type for Quantity multiplication.")
        
        # converts all units if necessary
        if Quantity.auto_format:
            return answer.converted_auto(list(self.unit_type.keys()))
        else:
            return answer
        
    def __rmul__(self, other: Union[Quantity, int, float]) -> Quantity:
        """
        Same as multiplication, but in reverse. 
        See documentation of __mul__() for more info about multiplication.
        """
        return self * other
    
    def __truediv__(self, other: Union[Quantity, int, float]) -> Quantity:
        """
        Arguments: a Quantity, or number to divide the Quantity by.

        Raises: a UnitError for unsupported units.

        Returns: a new Quantity object with the division being done.
        """

        new_types = self.unit_type.copy()

        if isinstance(other, (int, float)):

            # divides number and returns
            return Quantity(self.number / other, new_types)

        elif isinstance(other, Temperature):

            raise CompatabilityError("A Quantity (absolute temperature) is incompatible for addition with a Temperature (relative temperature)")

        elif isinstance(other, Quantity):

            # reverses dictionary
            new_types = {unit: - power for unit, power in other.unit_type.items()}
            new_num = 1 / other.number

            # performs multiplication with inverted object
            return self * Quantity(new_num, new_types)
    
    def __rtruediv__(self, other: Union[int, float, Quantity]) -> Quantity:

        """
        Arguments: a Quantity, or number to divide by the Quantity.

        Raises: a CompatabilityError for unsupported units.

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

        for key in list(self.unit_type.keys()):
            if self.unit_type[key] == 0:
                del self.unit_type[key]

    def __format_num(num: Union[int, float]) -> str:

        """
        Formats the number of a Quantity for printing.
        
        For example, 123456 with a precision of 2 becomes 1.23*10⁵.
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
        Arguments: An integer power to raise the number to.

        Returns: A string that contains the unit raised the power.
        """

        # start output with the unit
        output = unit.replace('deg. ', Temperature.DEG_SYMB)

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

        # adds degree symbol for temperatures
        return output
    
    def converted_auto(self, target_units: list) -> Quantity:

        """
        Arguments: A list of units to convert to. The program will try to convert the Quantity to each unit provided in this list.

        Raises: UnitError for unsupported units.
        
        Returns: a new Quantity object with possible unit converted to the other_conversions, if possible.
        """

        output = self.__copy__()

        for conversion in target_units:
            for function in _CONVERT_FUNCS:
                try:
                    output = function(output, target=conversion)
                except:
                    continue

        return output

    def __converted(self, factors: dict, target: str, original: str = None) -> Quantity:

        """
        Arguments: a dictionary of conversion factors in this format: {'supported': LIST1, 'to': DICT1, 'from': DICT2}, 
        where units are the supported units for the conversion. Also takes in the target unit and original unit. 
        If original is not entered, it is automatically interpreted.
        
        Returns: a new Quantity with the conversion being done on it.
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

    @__register_conversion
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
    
    @__register_conversion
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

    @__register_conversion
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
    
    @__register_conversion
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
    
    @__register_conversion
    def converted_temperature(self, target: str, original: str = None) -> Quantity:
        
        """
        Note: This is for absolute temperature conversions. For example, if you wanted to see what an increase in 10 K corresponded to in degrees F, or something of the sort.

        Arguments: an original unit and a target unit. If original is not entered, it is automatically interpreted.

        Raises: a UnitError if the unit entered is not supported.

        Returns: a new Quantity object, with the original unit converted to the target unit. 
        """

        return self.__converted(factors = {
            'supported': TEMPERATURE_UNITS,
            'to': CONVERT_TO_CELSIUS,
            'from': CONVERT_FROM_CELSIUS
        }, target=target, original=original)
    
    def standardized_physics(self) -> Quantity:

        """
        Converts the Quantity to standard SI units (meters, seconds, kilograms, etc.).

        Returns a new Quantity with converted measurements.
        """

        return self.converted_auto(Quantity._PHYSICS_UNITS)

    def standardized_chemistry(self) -> Quantity:

        """
        Converts the Quantity to standard units for chemistry (meters, seconds, grams, etc.).

        Returns a new Quantity with converted measurements
        """

        return self.converted_auto(Quantity._CHEMISTRY_UNITS)

class Temperature:

    """
    This class is for relative, rather than absolute temperatures. 
    While looking at absolute temperatures, an increase in 45 Fahrenheit corresponds to an increase in 25 Kelvin or 25 Celsius.
    However, in relative temperatures, based around the boiling point of water, 0 Celsius is 273 Kelvin.
    Note: Temperature arithmetic (adding, subtracting) is supported, but uses absolute temperature changes rather than relative. 
    For example, 2 deg. F - 0 deg. C returns 2 deg. F rather -30 deg. F.
    """

    DEG_SYMB = "°"

    precision = 2

    def set_precision(new_precision: int):
        """
        Changes the number of decimal to round to.
        """
        if not isinstance(new_precision, int):
            raise TypeError("Precision must be an integer.")
        
        Temperature.precision = new_precision

    def __init__(self, number: Union[int, float], type: str):

        """
        Note: For a description of the class itself, type just the class out and hover over it.

        Arguments: Number (number for the temperature), type of the temperature (enter 'C', 'K', or 'F').
        Quantity objects can have temperature units, but they are only converted using absolute temperatures. 
        Temperature objects are converted using relative temperatures.

        Raises: UnitError if there is a wrong unit of measurement.
        """

        if type not in TEMPERATURE_UNITS:
            raise UnitError(f"Invalid unit of measurement for a temperature: '{type}'")

        self.type = type
        self.number = number

    def __str__(self) -> str:
        """
        Returns the temperature in the form <number> <symbol>. For example, '100 K' or '50°F'.
        """
        symbol = self.type.replace('deg. ', Temperature.DEG_SYMB)
        return f"{round(self.number, Temperature.precision)} {symbol}"
    
    def __copy__(self) -> Temperature:

        """
        Returns a copy of the Temperature.
        """

        return Temperature(self.number, self.type)
    
    def __mul__(self, other: Union[int, float]) -> Temperature:

        """
        Arguments: a number to multiply the current temperature by.

        Raises: UnsupportedError for classes unsupported with multiplication.

        Returns: a Temperature object, if multiplied with a number.
        """

        # new temperature with multiplication done
        if isinstance(other, (float, int)):
            return Temperature(self.number * other, self.type)
        else:
            raise UnsupportedError("Unsupported type for multiplication with Temperature.")
            
    def __rmul__(self, other: Union[int, float]) -> Temperature:

        """
        Performs multiplcation as defined in __mul__().
        """

        return self * other
    
    def __add__(self, other: Temperature) -> Temperature:

        """
        Arguments: Another temperature object to add to self.

        Raises: TypeError for wrong types (anything other than Temperature).

        Returns: A new Temperature object - the sum.
        """

        # detects for incorrect type
        if not isinstance(other, Temperature):
            raise TypeError("Only Temperature objects can be added to Temperatre objects.")

        # converts other to the same type and then returns
        return Temperature(self.number + CONVERT_TO_CELSIUS[other.type] * CONVERT_FROM_CELSIUS[self.type] * other.number, self.type)
    
    def __radd__(self, other: Temperature) -> Temperature:

        """
        Simply reversed addition. See __add__() for more information.
        """

        return other + self
    
    def __sub__(self, other: Temperature) -> Temperature:

        """
        Arguments: Another temperature object to subtract from self.

        Raises: TypeError for wrong types (anything other than Temperature).

        Returns: A new Temperature object - the difference.
        """

        return self + (-1 * other)
    
    def __rsub__(self, other: Temperature) -> Temperature:

        """
        Back-up method for subtracting. See __sub__() for more information.
        """

        return other + (-1 * self)
    
    def __pow__(self, power: int) -> UnsupportedError:

        """
        Raises UnsupportedError, because Temperature do not support being multiplied by other units.
        """

        raise UnsupportedError("Cannot raise relative Temperatures to a power. Try using a Quantity object instead.")
    
    def to_quantity(self) -> Quantity:

        """
        Returns the Temperature as a Quantity object.
        """

        return Quantity(self.number, {self.type: 1})
        
    @property
    def celsius(self) -> Union[int, float]:
        """
        Returns the number part of the temperature in degrees Celsius.
        """
        if self.type == 'deg. C':
            return self.number
        elif self.type == 'deg. F':
            return (self.number - 32) * 5 / 9
        elif self.type == 'K':
            return self.number - 273
        
    @property
    def fahrenheit(self) -> Union[int, float]:
        """
        Returns the number part of the temperature in degrees Fahrenheit.
        """
        if self.type == 'deg. F':
            return self.number
        elif self.type == 'deg. C':
            return self.number * (9 / 5) + 32
        elif self.type == 'K':
            return (self.number + 273) * (9 / 5) + 32
        
    @property
    def kelvin(self) -> Union[int, float]:
        """
        Returns the number part of the temperature in Kelvin.
        """ 
        if self.type == 'K':
            return self.number
        elif self.type == 'deg. C':
            return self.number + 273
        elif self.type == 'deg. F':
            return (self.number - 32) * (5 / 9) + 273
    
    def converted(self, target: str):
        """
        Arguments: A single character representing the unit of the target temperature (eg 'K' or 'F').

        Raises: UnitError for a wrong temperature unit.

        Returns: A new Temperature with the updated unit.
        """

        # check for invalid
        if target not in TEMPERATURE_UNITS:
            raise UnitError(f"Target unit '{target}' is not a supported temperature.")
        
        # perform number conversion
        if target == 'K':
            number = self.kelvin
        elif target == 'deg. C':
            number = self.celsius
        elif target == 'deg. F':
            number = self.fahrenheit

        # update type
        type = target

        return Temperature(number, type)
    
class Element:

    """
    Uses data from @Bowserinator to obtain data about chemical elements.
    """

    # loads symbols and numbers
    with open(f"{Path(__file__).parent}/periodic/periodic-table-symbols.json", "r") as f:
        _SYMBOL_TO_NAME = json.load(f)
    with open(f"{Path(__file__).parent}/periodic/periodic-table-numbers.json") as f:
        _NUMBER_TO_NAME = json.load(f)

    def __init__(self, element_symbol: str = None, element_name: str = None, element_number: int = None) -> Element:

        """
        Arguments: EITHER a symbol OR a name for the element. 

        Raises: ArgumentError for when both or neither the symbol and name are given.
        NameError for incorrect symbol or name.

        Returns: a new Element
        """

        if [element_symbol, element_name, element_number].count(None) != 2:
            raise ArgumentError("You must enter only one of the folloing: a name, symbol, or number.")

        # obtain json data for the element
        with open(f"{Path(__file__).parent}/periodic/periodic-table-lookup.json", "r") as f:
            table = json.load(f)
            try:
                if element_name:
                    self.information = table[element_name.lower()]  # format name to lowercase: "Hydrogen" -> "hydrogen"
                elif element_number: 
                    self.information = table[Element._NUMBER_TO_NAME[str(element_number)]]
                elif element_symbol:
                    self.information = table[Element._SYMBOL_TO_NAME[element_symbol]]
            except:
                raise ArgumentError("Invalid information given. Check your spelling.")

    """
    Below are several properties of the element, returned via information lookup.
    """     

    @property
    def name(self) -> str:
        """
        Returns the name of the element, capitalized.
        """
        return self.information["name"]
    
    @property
    def symbol(self) -> str:
        """
        Returns the element symbol.
        """
        return self.information["symbol"]
    
    @property 
    def desc(self) -> str:
        """
        Returns a short description of the element.
        """
        return self.information["summary"]
    
    @property
    def discoverer(self) -> str:
        """
        Returns the name of the person who discovered the element.
        """
        return self.information["discovered_by"]
    
    @property
    def mass(self) -> Quantity:
        """
        Returns the atomic mass of the element as a Quantity object
        """
        return Quantity(self.information["atomic_mass"], {"g": 1, "mol": -1})
    
    @property
    def state(self) -> str:
        """
        Returns the state of the element at room temperature.
        """
        return self.information["state"]
    
    @property 
    def density(self) -> Quantity:
        """
        Returns the density of the element at room temperature. in g/L if gas, otherwise in g/mL
        """
        if self.state == "Gas":
            return Quantity(self.information["density"], {"g": 1, "L": -1})
        else:
            return Quantity(self.information["density"], {"g": 1, "mL": -1})
        
    @property
    def boiling_point(self) -> Quantity:
        """
        Returns the boiling point in Kelvin.
        """
        return Quantity(self.information["boil"], {'K': 1})
    
    @property
    def melting_point(self) -> Quantity:
        """
        Returns the melting point in Kelvin.
        """
        return Quantity(self.information["melt"], {'K': 1})
    
    @property 
    def period(self) -> int:
        """
        Returns the period of the element.
        """
        return self.information["period"]
    
    @property 
    def group(self) -> int:
        """
        Returns the group (column) of the element.
        """
        return self.information["group"]
    
    @property
    def number(self) -> int:
        """
        Returns the atomic number of the element.
        """
        return self.information["number"]
    
    @property
    def electron_config_str(self) -> str:
        """
        Returns the element's electron configuration as a string. 
        For example, for lithium, "1s2 2s1" is outputted
        """
        return self.information["electron_configuration"]

    @property
    def electron_config(self) -> dict:
        """
        Returns a dictionary of electron orbitals and electrons within those orbitals.
        Example: {"1s": 2, "2s": 1}
        Use element.electron_config_str to get a string format, like "1s2 2s1"
        """
        list_configs = self.electron_config_str.split()
        configs = {}

        # converts "1s2" to "1s": 2
        for config in list_configs:
            configs[config[:2:]] = int(config[2::])
        
        return configs



