from decimal import Decimal
from typing import Callable

class Calculation:
    def __init__(self, val1: Decimal, val2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        self.val1 = val1
        self.val2 = val2
        self.operation = operation
        self.result = None  # result not computed yet

    def perform(self) -> Decimal:
        if self.operation.__name__ == "divide" and self.val2 == 0:
            raise ValueError("Cannot divide by zero")
        self.result = self.operation(self.val1, self.val2)
        return self.result

    def __repr__(self):
        # No result shown here, matching your test expectations
        return f"Calculation({self.val1}, {self.val2}, {self.operation.__name__})"
