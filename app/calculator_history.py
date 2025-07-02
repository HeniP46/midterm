import pandas as pd
import os
import logging

# Configure logging from environment variable or default to INFO
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

class CalculatorHistory:
    """Handles loading, saving, and modifying calculator history using a CSV file."""

    def __init__(self, file_path=None):
        self.file_path = file_path or os.environ.get("HISTORY_FILE", "data/calculator_history.csv")
        self.history = []
        self.max_size = 5
        self._load_from_file()

    def _load_from_file(self):
        """Load calculation history from file using LBYL and EAFP."""
        # LBYL: Check if file exists before trying to load
        if os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)  # EAFP inside
                self.history = df.to_dict(orient="records")
                logging.info(f"Calculator history loaded from {self.file_path}.")
            except Exception as e:
                logging.error(f"Failed to load history from file: {e}")
                self.history = []
        else:
            logging.warning(f"History file not found at {self.file_path}. Starting with empty history.")
            self.history = []

    def add_calculation(self, operation, num1, num2, result):
        """Adds a new calculation."""
        if self.max_size and len(self.history) >= self.max_size:
            raise Exception("Cannot add more than 5 calculations.")

        calc_dict = {
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result
        }

        self.history.append(calc_dict)
        logging.info(f"Added calculation: {calc_dict}")
        self._save_to_file()

    def remove_calculation(self, index):
        """Remove calculation at the given index."""
        if 0 <= index < len(self.history):  # LBYL: check first
            removed = self.history.pop(index)
            logging.info(f"Removed calculation at index {index}: {removed}")
            self._save_to_file()
        else:
            raise IndexError("Invalid index for removal.")

    def _save_to_file(self):
        """Save current history to file using EAFP."""
        try:
            df = pd.DataFrame(self.history)
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            df.to_csv(self.file_path, index=False)
            logging.info(f"Calculator history saved to {self.file_path}.")
        except Exception as e:
            logging.error(f"Failed to save history to file: {e}")

    def list_calculations(self):
        """Return the current list of calculations."""
        return self.history
