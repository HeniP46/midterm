from decimal import Decimal
from typing import Callable

class Calculation:
    def __init__(self, val1: Decimal, val2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        self.val1 = val1
        self.val2 = val2
        self.operation = operation

    def perform(self) -> Decimal:
        if self.operation.__name__ == "divide" and self.val2 == 0:
            raise ValueError("Cannot divide by zero")
        return self.operation(self.val1, self.val2)

    def __repr__(self):
        return f"Calculation({self.val1}, {self.val2}, {self.operation.__name__})"
