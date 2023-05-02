Documentation
=============

Below is documentation for the various features in this module!

.. _Supported Conversions:

Supported Conversions
---------------------

Metric Conversions
~~~~~~~~~~~~~~~~~~

Below are the supported metric prefixes handled in this package:

.. code:: python

    'y': 1e-24
    'z': 1e-21
    'a': 1e-18
    'f': 1e-15
    'p': 1e-12
    'n': 1e-9
    'µ': 1e-6
    'mc': 1e-6      # for those who cannot use the µ symbol
    'm': 1e-3
    'c': 1e-2
    'd': 1e-1
    'da': 1e1
    'h': 1e2
    'k': 1e3
    'M': 1e6
    'G': 1e9
    'T': 1e12
    'P': 1e15
    'E': 1e18
    'Z': 1e21
    'Y': 1e24

And here are the supported units for converting metric:

.. code:: python

    's', 'm', 'g', 'K', 'mol', 'J', 'W', 'N', 'Pa', 'L'

Conversion Factors
~~~~~~~~~~~~~~~~~~

Below is a list of supported units for conversions for each conversion type. It contains the unit, followed by its conversion factor to the chosen reference unit for the conversion group (conversion factor is simply what you multiply a measurement in that unit by to get the number of reference units).

Length Conversions
++++++++++++++++++

The reference unit used for this is meters.

.. code:: python

    'ft': 0.3048    # feet
    'yd': 0.9144    # yards
    'in': 0.0254    # inches
    'mi': 1609      # miles
    'ly': 946e13    # light years
    'au': 1496e8    # astronomical units
    'pc': 31e15     # parsecs
    'm': 1          # meters

Weight / Mass Conversions
+++++++++++++++++++++++++

The reference unit used for this is grams.

.. code:: python

    'g': 1              # grams
    'lb': 454           # pounds
    'oz': 454 / 16      # ounces
    'st': 6356          # stones
    'amu': 1.661e-24    # atomic mass units

Time Conversions
++++++++++++++++

The reference unit used for this is seconds.

.. code:: python

    's': 1                          # seconds
    'min': 60                       # minutes
    'hr': 3600                      # hours
    'dy': 3600 * 24                 # days
    'wk': 3600 * 24 * 7             # weeks
    'yr': 3600 * 24 * 365.25    # year

Volume Conversions
++++++++++++++++++

The reference unit used for this is liters.

.. code:: python

    'L': 1                  # liters
    'c.': 0.2366,           # cups
    'pt.': 0.2366 * 2       # pints
    'qt.': 0.2366 * 4       # quarts
    'gal.': 0.2366 * 16     # gallons
    'fl. oz': 0.2366 / 8    # fluid ounces
    'tbsp': 0.2366 / 16     # tablespoons
    'tsp': 0.2366 / 48      # teaspoons

Temperature Conversions
+++++++++++++++++++++++

The reference unit used for this is Kelvin. Note: these are absolute temperature conversions (not in reference to the boiling point of water like traditional Celsius and Fahrenheit)

.. code:: python

    'deg. C': 1             # degrees Celsius
    'deg. F': 5 / 9         # degrees Fahrenheit
    'K': 1                  # Kelvin

Pressure Conversions
++++++++++++++++++++

The reference unit used for this is the atm.

.. code:: python

    'atm': 1                # atmospheres
    'torr': 0.0013157       # torr
    'mm Hg': 0.0013157      # millimeters mercury
    'bar': 0.986923         # bars
    'Pa': 0.0000098         # pascals
    'psi': 0.068046         # pounds per cubed inch

Quantity
--------

This is the class that will manage most of your conversions. To import this, you can run either of the following:

.. code:: python

    from unisci import Quantity
    from unisci.types import Quantity

You can create a Quantity using a constructor in the following format: 

.. code:: 

    Quantity(<value>, <dict>)

Where <value> is the numerical value of the Quantity and <dict> is a dictionary of units and their powers. For example, here is the initialization of a Quantity holding the value :code:`1.0 m/s²`.

.. code:: python

    length = Quantity(1, {'m': 1, 's': -2})
    print(length)

.. code:: 

    1.000*10⁰ m/s²

Below are methods associated with this class. :code:`quan` represents an arbitrary Quantity object.

:code:`Quantity.set_precision()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Quantity.set_precision(number: int) -> None

Sets the precision (number of decimal places) of printing output. The default value is 3, which is why the above example prints :code:`1.000` rather than :code:`1.0`. The below example sets the precision to 2 decimal places.

.. code:: python

    Quantity.set_precision(number=2)

:code:`Quantity.set_auto_format()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Quantity.set_auto_format(do: bool) -> None

Determines if the auto-conversions should be done. For example, when multiplying Quantity's with units :code:`m` and :code:`in`, if :code:`auto_format` is enabled, the product will be in the units of the first number. It also enables auto-condensation of complicated units, which will be elaborated upon further regarding the :code:`x.simplified()` method.

.. code:: python

    >>> length_m = Quantity(1, {'m': 1})
    >>> length_in = Quantity(40, {'in': 1})
    >>> print(length_m * length_in)
    '1.016*10⁰ m²'
    >>> Quantity.set_auto_format(False)
    >>> print(length_m * length_in)
    '4.000*10¹ m-in'

:code:`quan.value`
~~~~~~~~~~~~~~~~~~

.. code:: python
    
    quan.value -> float

Returns the numerical value of the Quantity.

.. code:: python

    >>> x = Quantity(12, {'m': 1})
    >>> print(x.value)
    '12.0'

:code:`quan.units`
~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.units -> dict[str, int]

Returns a dictionary of units and powers of the Quantity's overall composition. Internally, the dictionary is stored as :code:`quan.unit_type`, but calling :code:`quan.units` is better because it returns a copy of the dictionary.

.. code:: python

    >>> x = Quantity(12, {'m': 1})
    >>> print(x.units)
    {'m': 1}

:code:`quan.converted()`
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.converted(target_units: list[str]) -> Quantity

Returns a Quantity converted to all the units it can in the provided list of target units. 

.. code:: python

    >>> velocity = Quantity(1, {'in': 1, 'min': -1})
    >>> print(velocity)
    '1.000*10⁰ in/min'
    >>> velocity = velocity.converted(['cm', 's'])
    >>> print(velocity)
    '4.233*10⁻² cm/s'

Supported units for conversion can be found in the :ref:`Supported Conversions` section.

:code:`quan.converted_metric()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.converted_metric(target: str, original: str) -> Quantity

Returns a new Quantity with metric conversions being done. This is useful for complex units that aren't supported in normal conversions, such as Newtons or Joules.

.. code:: python

    >>> energy = Quantity(1000, {'J': 1})
    >>> print(energy)
    '1.000*10³ J'
    >>> energy = energy.converted_metric(original='J', target='kJ')
    >>> print(energy)
    '1.000*10⁰ kJ'

Specific Conversions
~~~~~~~~~~~~~~~~~~~~

The following methods are available for specific conversions, although generally using :code:`quan.converted()` is better:

    * :code:`quan.converted_length()`
    * :code:`quan.converted_mass()`
    * :code:`quan.converted_time()`
    * :code:`quan.converted_volume()`
    * :code:`quan.converted_temperature()`
    * :code:`quan.converted_pressure()`

All of the following follow the same format:

.. code:: python

    quan.converted_function(target: str, original: str) -> Quantity

They take in a target unit and an optional original unit. If no original unit is entered, all compatible conversions will be done to the target unit. These are useful for when you want to convert only one kind of unit to the other, as shown here:

.. code:: python

    >>> weird_unit = Quantity(1, {'m': 1, 'ft': -1})
    >>> print(weird_unit)
    '1.000*10⁰ m/ft'
    >>> weird_unit = weird_unit.converted_length(original='ft', target='in')
    >>> print(weird_unit)
    '8.333*10⁻² m/in'

:code:`quan.simplified()`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.simplified() -> Quantity

Returns a Quantity with units automatically condensed into complex units. If `Quantity.auto_format` is set to True, this will happen automatically upon conversions or multiplications with other units.

.. code:: python

    >>> Quantity.set_auto_format(False)
    >>> force = Quantity(1, {'m': 1, 'kg': 1, 's': -2})
    >>> print(force)
    '1.000*10⁰ m-kg/s²'
    >>> print(force.simplified())
    '1.000*10⁰ N'

:code:`quan.force_simplified()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.force_simplified(target: str, exp: int = 1) -> Quantity

Forcibly converts a unit to the given target. Does this by multiplying by the inverse of the 'base units'.

.. code:: python

    >>> acceleration = Quantity(1, {'m': 1, 's': -2})
    >>> print(acceleration)
    '1.000*10⁰ m/s²'
    >>> print(acceleration.force_simplified(target='N', exp=1))
    '1.000*10⁰ N/kg'

:code:`quan.to_base_units()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.to_base_units() -> Quantity

Simplifies a Quantity's complicated units to their most 'basic' units.

.. code:: python

    >>> energy = Quantity(1, {'J': 1})
    >>> print(energy)
    '1.000*10⁰ J'
    >>> print(energy.to_base_units())
    '1.000*10⁰ kg-m²/s²'

Standardizing Functions
~~~~~~~~~~~~~~~~~~~~~~~

Here are the functions that are currently included in this package.

.. code:: python

    quan.standardized_physics() -> Quantity 
    quan.standardized_chemistry() -> Quantity

Standardizes a Quantity to the standard units in that discipline. Here are the converions made: 

.. code:: python

    PHYSICS_UNITS = ['m', 's', 'kg', 'L', 'K']
    CHEMISTRY_UNITS = ['m', 's', 'g', 'L', 'K', 'atm']

Here is an example:

.. code:: python

    >>> velocity = Quantity(1, {'ly': 1, 'yr': -1})
    >>> print(velocity)
    '1.000*10⁰ ly/yr'
    >>> print(velocity.standardized_physics())
    '2.998*10⁸ m/s'

Supported Operations
~~~~~~~~~~~~~~~~~~~~

Supported operations using the Quantity class involve:

    * Multiplication: With a number or a Quantity
    * Division: With a mumber or a Quantity
    * Addition: With a number (when Quantity is unitless) or a Quantity
    * Exponents: With an integer power

Here is an example of them in action:

.. code:: python

    >>> f1 = Quantity(1, {'N': 1})
    >>> m2 = Quantity(12, {'lb': 1})
    >>> a2 = Quantity(3, {'mi': 1, 'hr': -2})
    >>> print(f"{f1}, {m2}, {a2}")
    '1.000*10⁰ N, 1.200*10¹ lb, 3.000*10⁰ mi/hr²'
    >>> f2 = m2 * a2            # multiplication
    >>> print(f2)
    '3.600*10¹ lb-mi/hr²'
    >>> f3 = f1 + f2
    >>> print(f3)               # addition
    '1.002*10⁰ N'
    >>> m3 = Quantity(6.00, {'st': 1})
    >>> a3 = f3 / m3            # division
    >>> print(a3)
    '2.627*10⁻² m/s²'

