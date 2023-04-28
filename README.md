# UniSci

[![PyPi Version](https://badgen.net/pypi/v/unisci/)](https://pypi.org/project/unisci)

A module to perform unit conversions for almost any scientific topic! This package is available on PyPI [here](https://pypi.org/project/unisci/).

## Why Use This?
Short for "Unit Science", UniSci is primarilty focused on being able to use any unit and easily convert it to another. It supports automatic conversions for formulas, condensation of complex units like `kg-m/s²` to `N`, and more!

## Installation 
To install, simply run the following:
```
$ pip install unisci
```

Then, you can use it as you please!
```python
>>> from unisci import Quantity
>>> length = Quantity(1, {'m': 1})
>>> print(length.converted(['ft']))
3.281*10⁰ ft
```

## Use Cases
See some use cases in the `use_cases.ipynb` notebook, [here](https://github.com/vivaansinghvi07/conversions/blob/main/use_cases.ipynb).

## Documentation
Full documentation can be found on the [readthedocs](https://unisci.readthedocs.io/en/latest/index.html) site for the module.

## Contribution
For adding conversions, formulas, or more, pull requests are greatly appreciated. Feel free to message me on my email singhvi.vivaan@gmail.com if you have any concerns!

## License
This project is released under the MIT license.
