Documentation
=============

Below is documentation for the various features in this module!

:code:`Quantity`
----------------

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

Below are methods associated with this class. :code:`x` represents an arbitrary Quantity object.

:code:`Quantity.set_precision()`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

