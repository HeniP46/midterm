from decimal import Decimal
import pytest
from app.commands.add import AddCommand
from app.commands.subtract import SubtractCommand
from app.commands.multiply import MultiplyCommand
from app.commands.divide import DivideCommand

def test_add_command_name():
    cmd = AddCommand()
    assert cmd.name() == "add"

def test_add_command_execute():
    cmd = AddCommand()
    result = cmd.execute("2", "3")
    assert result == Decimal("5")

def test_subtract_command_name():
    cmd = SubtractCommand()
    assert cmd.name() == "subtract"

def test_subtract_command_execute():
    cmd = SubtractCommand()
    result = cmd.execute("5", "3")
    assert result == Decimal("2")

def test_multiply_command_name():
    cmd = MultiplyCommand()
    assert cmd.name() == "multiply"

def test_multiply_command_execute():
    cmd = MultiplyCommand()
    result = cmd.execute("4", "3")
    assert result == Decimal("12")

def test_divide_command_name():
    cmd = DivideCommand()
    assert cmd.name() == "divide"

def test_divide_command_execute():
    cmd = DivideCommand()
    result = cmd.execute("10", "2")
    assert result == Decimal("5")

def test_divide_by_zero_raises():
    cmd = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        cmd.execute("5", "0")