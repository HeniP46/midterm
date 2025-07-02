from decimal import Decimal
from app.command import Command

class PowerCommand(Command):
    def name(self) -> str:
        return "power"

    def execute(self, a: float, b: float) -> Decimal:
        return Decimal(str(a)) ** Decimal(str(b))
