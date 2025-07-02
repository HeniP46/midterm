# calculator

A Python-based command-line calculator that supports basic operations, dynamic plugin loading, history tracking with Pandas, environment-based configuration, and professional logging.

---

## Setup Instructions

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```
HISTORY_FILE=data/calculator_history.csv
LOG_LEVEL=INFO
```

To run the calculator:

```bash
python main.py
```

To run tests:

```bash
pytest --cov=app
```

---

## Usage

* `add 3 5`, `subtract 10 4`, `multiply 2 6`, or `divide 8 2`.
* Use `menu` to view available commands.
* Use `remove <index>` to delete a specific calculation from history.
* Use `exit` to quit.

---

## Environment Variable Usage

* `HISTORY_FILE` (used in `app/__init__.py` and `calculator_history.py`) sets where your history CSV is stored.
* `LOG_LEVEL` (used in `calculator_history.py`) dynamically sets the log level (`DEBUG`, `INFO`, `WARNING`, etc.).

---

## Logging Strategy

Logging is controlled by the `LOG_LEVEL` environment variable.

* `INFO` for normal events like adding/removing history (e.g., history loaded, saved).
* `WARNING` if the file is missing.
* `ERROR` for exceptions (like file save/load failure).

Examples:

```python
logging.info("Calculator history loaded from file")
logging.warning("History file not found")
logging.error("Failed to save history")
```

Found in `calculator_history.py`, `app/__init__.py`.

---

## Design Patterns Used

### Command Pattern

* Each operation (add, subtract, etc.) is a class with an `execute` method.
* Example: `app/commands/add.py`, `subtract.py`, etc.

### Facade Pattern

* `CalculatorHistory` hides internal logic of using Pandas for history.
* Found in `calculator_history.py`.

### Factory Method

* Commands are loaded dynamically via `plugin_loader.load_commands()`.
* Found in `plugin_loader.py`.

### ingleton Pattern

* Logging is configured once globally at app startup.
* Found in `calculator_history.py`, `app/__init__.py`.

### Strategy Pattern

* Each command class provides its own `execute` logic following a common interface.

---

## Exception Handling

### LBYL (Look Before You Leap)

* In `app/__init__.py`, user input is checked before processing:

```python
if len(parts) != 3:
    print("Invalid input. Usage: <command> <num1> <num2>")
```

* In `calculator_history.py`:

```python
if os.path.exists(self.file_path):
    # load history
```

### EAFP 

* Also in `app/__init__.py`, command execution wrapped in try/except:

```python
try:
    result = commands[command_name].execute(arg1, arg2)
except Exception as e:
    print(f"Error: {e}")
```

* File save in `calculator_history.py`:

```python
try:
    df.to_csv(self.file_path, index=False)
except Exception as e:
    logging.error(f"Failed to save history to file: {e}")
```

## Demo Video
https://youtu.be/NssXdXJWXEg
