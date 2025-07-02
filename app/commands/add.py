from decimal import Decimal
from app.command import Command

class AddCommand(Command):
    def name(self) -> str:
        return "add"

    def execute(self, a: float, b: float) -> Decimal:
        return Decimal(str(a)) + Decimal(str(b))
