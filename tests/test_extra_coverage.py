import pytest
from app import App
from app.commands.add import AddCommand
from app.commands.subtract import SubtractCommand
from app.commands.multiply import MultiplyCommand
from app.commands.divide import DivideCommand
from app import plugin_loader

def test_app_empty_input_then_exit(monkeypatch, capfd):
    inputs = iter(['', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    App.start()
    out, err = capfd.readouterr()
    assert "Please enter a command." in out
    assert "Exiting..." in out

def test_command_names():
    assert AddCommand().name() == "add"
    assert SubtractCommand().name() == "subtract"
    assert MultiplyCommand().name() == "multiply"
    assert DivideCommand().name() == "divide"

def test_divide_by_zero():
    cmd = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        cmd.execute("5", "0")

def test_load_commands_returns_dict():
    commands = plugin_loader.load_commands()
    assert isinstance(commands, dict)
    assert "add" in commands
    assert "subtract" in commands
    assert "multiply" in commands
    assert "divide" in commands