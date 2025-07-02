from decimal import Decimal
from app.command import Command

class MultiplyCommand(Command):
    def name(self) -> str:
        return "multiply"

    def execute(self, a: float, b: float) -> Decimal:
        return Decimal(str(a)) * Decimal(str(b))
