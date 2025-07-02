from decimal import Decimal
from app.command import Command

class SubtractCommand(Command):
    def name(self) -> str:
        return "subtract"

    def execute(self, a: float, b: float) -> Decimal:
        return Decimal(str(a)) - Decimal(str(b))
