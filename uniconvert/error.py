# error message for invalid quantities
class UnitError(Exception):
    def __init__(self, message):
        self.message = message

# for incompatible units and/or Quantities
class CompatabilityError(Exception):
    def __init__(self, message):
        self.message = message
    
# for operations not supported
class UnsupportedError(Exception):
    def __init__(self, message):
        self.message = message

# for arguments being entered incorrectly
class ArgumentError(Exception):
    def __init__(self, message):
        self.message = message