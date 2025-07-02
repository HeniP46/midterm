import os
import logging
from app.calculator_history import CalculatorHistory
from app.plugin_loader import load_commands

def configure_logging():
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_output = os.getenv("LOG_OUTPUT", "console").lower()

    log_level = getattr(logging, log_level_str, logging.INFO)
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    if log_output == "file":
        logging.basicConfig(
            filename="calculator.log",
            level=log_level,
            format=log_format
        )
    else:
        logging.basicConfig(
            level=log_level,
            format=log_format
        )

configure_logging()

class App:
    MAX_HISTORY = 5

    @staticmethod
    def start():
        logging.info("Starting calculator app...")

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
                logging.info("EOF received. Exiting.")
                print("\nExiting...")
                break

            if not user_input:
                print("Please enter a command.")
                continue

            if user_input.lower() == "exit":
                logging.info("User exited the application.")
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
                    logging.warning("Remove command used with non-numeric index.")
                    print("Invalid index.")
                    continue
                index = int(index_str)
                try:
                    history.remove_calculation(index)
                    logging.info(f"Removed calculation at index {index}")
                except IndexError:
                    logging.warning(f"Tried to remove invalid index: {index}")
                    print("Invalid index.")
                except Exception as e:
                    logging.error(f"Error removing calculation: {e}")
                    print(f"Error removing calculation: {e}")
                continue

            parts = user_input.split()
            if len(parts) != 3:
                logging.warning("Invalid command format entered.")
                print("Invalid input. Usage: <command> <num1> <num2>")
                continue

            command_name, arg1_str, arg2_str = parts

            if command_name not in commands:
                logging.warning(f"Unknown command entered: {command_name}")
                print("Unknown command")
                continue

            try:
                arg1 = float(arg1_str)
                arg2 = float(arg2_str)
            except ValueError:
                logging.warning(f"Invalid numeric input: '{arg1_str}', '{arg2_str}'")
                print("Error: Invalid numeric input")
                continue

            try:
                result = commands[command_name].execute(arg1, arg2)

                if hasattr(history, "history") and isinstance(history.history, list):
                    if len(history.history) >= App.MAX_HISTORY:
                        logging.warning("History limit reached.")
                        print("History limit reached. Please remove some entries.")
                        continue

                result = int(result) if result == int(result) else result
                print(f"Result: {result}")
                logging.info(f"Executed {command_name}({arg1}, {arg2}) = {result}")
                history.add_calculation(command_name, arg1, arg2, result)

            except ZeroDivisionError:
                logging.warning("Division by zero attempted.")
                print("Error: Cannot divide by zero")
            except Exception as e:
                logging.error(f"Unexpected error during execution: {e}")
                print("Error: " + str(e))
