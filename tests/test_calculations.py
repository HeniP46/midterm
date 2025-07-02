import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.operations import add, divide  # import your operations

@pytest.mark.parametrize(
    "val1, val2, operation, expected",
    [
        (Decimal("10"), Decimal("5"), add, Decimal("15")),
        (Decimal("9"), Decimal("3"), divide, Decimal("3")),
        (Decimal("2"), Decimal("3"), add, Decimal("5")),
        (Decimal("6"), Decimal("2"), divide, Decimal("3")),
    ],
)
def test_calculation_operations(val1, val2, operation, expected):
    calc = Calculation(val1, val2, operation)
    result = calc.perform()  # perform explicitly to compute
    assert result == expected

def test_calculation_repr():
    calc = Calculation(Decimal("10"), Decimal("5"), add)
    assert repr(calc) == "Calculation(10, 5, add)"

def test_divide_by_zero():
    calc = Calculation(Decimal("10"), Decimal("0"), divide)
    with pytest.raises(ValueError):
        calc.perform()
