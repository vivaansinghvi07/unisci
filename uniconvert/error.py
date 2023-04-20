# error message for invalid quantities
class UnitError(Exception):
    def __init__(self, message):
        self.message = message

class CompatabilityError(Exception):
    def __init__(self, message):
        self.message = message