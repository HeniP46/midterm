from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env

history_path = os.getenv('HISTORY_FILE_PATH')
print(f'HISTORY_FILE_PATH is: {history_path}')