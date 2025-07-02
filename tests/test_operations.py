from decimal import Decimal
from app.operations import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(Decimal("2"), Decimal("3")) == Decimal("5")

def test_subtract():
    assert subtract(Decimal("5"), Decimal("2")) == Decimal("3")

def test_multiply():
    assert multiply(Decimal("4"), Decimal("2")) == Decimal("8")

def test_divide():
    assert divide(Decimal("10"), Decimal("2")) == Decimal("5")

def test_divide_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(Decimal("1"), Decimal("0"))
