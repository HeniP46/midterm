import os
from dotenv import load_dotenv
from app.calculator_history import CalculatorHistory

class App:
    @staticmethod
    def start():
        load_dotenv()
        history_file = os.getenv('HISTORY_FILE_PATH')
        calc_history = CalculatorHistory(history_file)

        print("App started with calculator history loaded.")