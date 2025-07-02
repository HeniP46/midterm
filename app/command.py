from abc import ABC, abstractmethod
from decimal import Decimal

class Command(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, a: str, b: str) -> Decimal:
        pass
