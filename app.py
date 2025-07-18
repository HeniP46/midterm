import os
import sys
import logging
from dotenv import load_dotenv
from app.calculator_history import CalculatorHistory

class App:
    @staticmethod
    def start():
        # Load environment variables from .env file
        load_dotenv()

        # Read environment variables
        history_file = os.getenv('HISTORY_FILE')
        log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_output = os.getenv('LOG_OUTPUT', 'console').lower()

        # Map log level string to logging module level
        log_level = getattr(logging, log_level_str, logging.INFO)

        # Configure logging based on environment variable LOG_OUTPUT
        if log_output == 'file':
            # Ensure directory exists for log file
            log_path = 'calculator.log'
            os.makedirs(os.path.dirname(log_path) or '.', exist_ok=True)
            logging.basicConfig(
                filename=log_path,
                level=log_level,
                format='%(asctime)s [%(levelname)s] %(message)s',
                filemode='a'
            )
        else:
            # Log to console/stdout
            logging.basicConfig(
                stream=sys.stdout,
                level=log_level,
                format='%(asctime)s [%(levelname)s] %(message)s'
            )

        logging.info(f"Logging started with level {log_level_str} and output {log_output}")
        logging.info(f"Using history file at: {history_file}")

        # Initialize calculator history with the file path from env
        calc_history = CalculatorHistory(history_file)

        print("App started with calculator history loaded.")
        logging.info("CalculatorHistory loaded successfully.")

        # Print loaded history entries for debugging
        for i, entry in enumerate(calc_history.list_calculations()):
            print(f"{i}: {entry['operation']}({entry.get('num1')}, {entry.get('num2')}) = {entry['result']}")
            logging.debug(f"History entry {i}: {entry}")

        # You can add your REPL loop or other app logic here
