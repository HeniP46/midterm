import os
import logging
from app.calculator_history import CalculatorHistory
from app.plugin_loader import load_commands

logging.basicConfig(level=logging.INFO)

class App:
    MAX_HISTORY = 5

    @staticmethod
    def start():
        history_file = os.environ.get("HISTORY_FILE")
        if not history_file:
            logging.error("HISTORY_FILE environment variable not set.")
            print("Error: HISTORY_FILE environment variable not set.")
            return

        os.makedirs(os.path.dirname(history_file), exist_ok=True)

        history = CalculatorHistory(history_file)
        commands = load_commands()

        print("Hello World. Type 'exit' to exit.")
        print("Available commands:", ", ".join(commands.keys()))
        print("Type 'remove <index>' to delete a calculation.")

        while True:
            try:
                user_input = input("> ").strip()
            except EOFError:
                print("\nExiting...")
                break

            if not user_input:
                print("Please enter a command.")
                continue

            if user_input.lower() == "exit":
                print("Exiting...")
                break

            if user_input.lower() == "menu":
                print("Available commands:", ", ".join(commands.keys()))
                print("Type 'remove <index>' to delete a calculation.")
                continue

            if user_input.lower().startswith("remove"):
                parts = user_input.split()
                if len(parts) != 2:
                    print("Usage: remove <index>")
                    continue
                index_str = parts[1]
                if not index_str.isdigit():
                    print("Usage: remove <index>")
                    print("Invalid index.")
                    continue
                index = int(index_str)
                try:
                    history.remove_calculation(index)
                except IndexError:
                    print("Invalid index.")
                except Exception as e:
                    print(f"Error removing calculation: {e}")
                continue

            parts = user_input.split()
            if len(parts) != 3:
                print("Invalid input. Usage: <command> <num1> <num2>")
                continue

            command_name, arg1_str, arg2_str = parts

            if command_name not in commands:
                print("Unknown command")
                continue

            try:
                arg1 = float(arg1_str)
                arg2 = float(arg2_str)
            except ValueError:
                print("Error: Invalid numeric input")
                continue

            try:
                result = commands[command_name].execute(arg1, arg2)

                result = int(result) if result == int(result) else result
                print(f"Result: {result}")

                # Only enforce history limit if real list exists
                if hasattr(history, "history") and isinstance(history.history, list):
                    if len(history.history) >= App.MAX_HISTORY:
                        print("History limit reached. Please remove some entries.")
                        continue

                history.add_calculation(command_name, arg1, arg2, result)
            except ZeroDivisionError:
                print("Error: Cannot divide by zero")
            except Exception as e:
                print("Error: " + str(e))
