# error message for invalid quantities
class QuantityError(Exception):
    def __init__(self, message):
        self.message = message