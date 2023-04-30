Documentation
=============

Below is documentation for the various features in this module!

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
    'yr': 3600 * 24 * 7 * 365.25    # year

Volume Conversions
++++++++++++++++++

The reference unit used for this is liters.

.. code:: python

    'L': 1                  # liters
    'c.': 0.2366,           # cups
    'pt.': 0.2366 * 2,      # pints
    'qt.': 0.2366 * 4,      # quarts
    'gal.': 0.2366 * 16,    # gallons
    'fl. oz': 0.2366 / 8,   # fluid ounces
    'tbsp': 0.2366 / 16,    # tablespoons
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

Quantity Class
--------------

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

:code:`quan.converted()`
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    quan.converted(target_units: list[str]) -> Quantity

Returns a Quantity converted to all the units it can in the provided list of target units. 

.. code:: python

    from unisci import Quantity
    length = Quantity(1, {'m': 1})
    print(length.converted(['ft']))

.. code::

    3.281*10⁰ ft

Supported units for conversion can be found below.