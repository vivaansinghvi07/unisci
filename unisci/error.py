class UnitError(Exception):
    """
    for invalid quantities
    """
    def __init__(self, message):
        self.message = message

class CompatabilityError(Exception):
    """
    for incompatible units and/or Quantities
    """
    def __init__(self, message):
        self.message = message
    
class UnsupportedError(Exception):
    """
    for operations not supported
    """
    def __init__(self, message):
        self.message = message

class ArgumentError(Exception):
    """
    for arguments being entered incorrectly
    """
    def __init__(self, message):
        self.message = message