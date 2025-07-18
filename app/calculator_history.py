import os
import logging
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
log_output = os.environ.get("LOG_OUTPUT", "console")
history_file_path = os.environ.get("HISTORY_FILE", "data/calculator_history.csv")

# Configure logging
if log_output == "file":
    logging.basicConfig(
        filename="calculator.log",
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
else:
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


class CalculatorHistory:
    def __init__(self, file_path=None):
        self.file_path = file_path or history_file_path
        self.history = []
        self.max_size = 5
        logging.info(f"CalculatorHistory initialized with file: {self.file_path}")

        if not os.path.exists("data"):
            os.makedirs("data")
            logging.info("Created data directory.")

        if os.path.exists(self.file_path):
            self.load_history()

    def load_history(self):
        try:
            df = pd.read_csv(self.file_path)
            self.history = df.to_dict(orient="records")[-self.max_size:]
            logging.info(f"Loaded history from {self.file_path}")
        except Exception as e:
            logging.error(f"Failed to load history: {e}")

    def add_calculation(self, operation, num1, num2, result):
        if len(self.history) >= self.max_size:
            raise Exception("Cannot add more than 5 calculations.")

        self.history.append({
            "operation": operation,
            "num1": float(num1),
            "num2": float(num2),
            "result": float(result)
        })
        self.save_history()
        logging.info(f"Added calculation: {operation}({num1}, {num2}) = {result}")

    def remove_calculation(self, index):
        if 0 <= index < len(self.history):
            removed = self.history.pop(index)
            logging.info(f"Removed calculation at index {index}: {removed}")
            self.save_history()
        else:
            raise IndexError("Invalid index for removal.")

    def list_calculations(self):
        return self.history

    def save_history(self):
        try:
            df = pd.DataFrame(self.history)
            df.to_csv(self.file_path, index=False)
            logging.info(f"Saved history to {self.file_path}")
        except Exception as e:
            logging.error(f"Failed to save history: {e}")

    def get_history(self):
        # Alias for list_calculations if needed
        return self.list_calculations()
