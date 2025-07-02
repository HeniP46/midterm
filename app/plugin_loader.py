import os
import importlib
from app.command import Command

def load_commands():
    commands = {}
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")

    if not os.path.isdir(commands_dir):
        raise FileNotFoundError(f"Commands directory not found: {commands_dir}")

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"app.commands.{filename[:-3]}"
            module = importlib.import_module(module_name)

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                # Check subclass and not the base Command class itself
                if isinstance(attribute, type) and issubclass(attribute, Command) and attribute is not Command:
                    instance = attribute()
                    commands[instance.name()] = instance
    return commands
