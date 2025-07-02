from decimal import Decimal
from app.command import Command

class DivideCommand(Command):
    def name(self) -> str:
        return "divide"

    def execute(self, a: float, b: float) -> Decimal:
        denominator = Decimal(str(b))
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Decimal(str(a)) / denominator
