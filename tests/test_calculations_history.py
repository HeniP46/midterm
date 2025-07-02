import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.operations import add, divide
from app.calculations import Calculations

def make_calc(val1, val2, op):
    return Calculation(val1, val2, op)

def test_add_and_get_history():
    Calculations.clear_history()
    calc1 = make_calc(Decimal("1"), Decimal("2"), add)
    calc2 = make_calc(Decimal("10"), Decimal("5"), divide)
    Calculations.add_calculation(calc1)
    Calculations.add_calculation(calc2)
    history = Calculations.get_history()
    assert len(history) == 2
    assert history[0] == calc1
    assert history[1] == calc2

def test_clear_history():
    Calculations.clear_history()
    calc = make_calc(Decimal("3"), Decimal("4"), add)
    Calculations.add_calculation(calc)
    assert len(Calculations.get_history()) == 1
    Calculations.clear_history()
    assert Calculations.get_history() == []

def test_get_latest():
    Calculations.clear_history()
    assert Calculations.get_latest() is None
    calc1 = make_calc(Decimal("5"), Decimal("5"), add)
    Calculations.add_calculation(calc1)
    assert Calculations.get_latest() == calc1
    calc2 = make_calc(Decimal("2"), Decimal("2"), divide)
    Calculations.add_calculation(calc2)
    assert Calculations.get_latest() == calc2

def test_find_by_operation():
    Calculations.clear_history()
    calc_add = make_calc(Decimal("1"), Decimal("2"), add)
    calc_divide = make_calc(Decimal("10"), Decimal("5"), divide)
    calc_add2 = make_calc(Decimal("3"), Decimal("4"), add)
    Calculations.add_calculation(calc_add)
    Calculations.add_calculation(calc_divide)
    Calculations.add_calculation(calc_add2)
    found_add = Calculations.find_by_operation("add")
    found_divide = Calculations.find_by_operation("divide")
    assert calc_add in found_add
    assert calc_add2 in found_add
    assert calc_divide in found_divide
    assert all(calc.operation.__name__ == "add" for calc in found_add)
    assert all(calc.operation.__name__ == "divide" for calc in found_divide)
