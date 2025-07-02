import os
import tempfile
import pytest
from app.calculator_history import CalculatorHistory

@pytest.fixture
def temp_history_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        yield temp_file.name
    os.remove(temp_file.name)

def test_add_and_list_calculation(temp_history_file):
    history = CalculatorHistory(temp_history_file)
    history.add_calculation("add", 3.0, 4.0, 7.0)
    result = history.list_calculations()[0]
    assert result["operation"] == "add"
    assert result["num1"] == 3.0
    assert result["num2"] == 4.0
    assert result["result"] == 7.0

def test_max_size_limit(temp_history_file):
    history = CalculatorHistory(temp_history_file)
    for i in range(5):
        history.add_calculation("add", i, i, i + i)
    with pytest.raises(Exception, match="Cannot add more than 5"):
        history.add_calculation("add", 6, 6, 12)

def test_remove_valid_index(temp_history_file):
    history = CalculatorHistory(temp_history_file)
    history.add_calculation("add", 1.0, 2.0, 3.0)
    assert len(history.list_calculations()) == 1
    history.remove_calculation(0)
    assert len(history.list_calculations()) == 0

def test_remove_invalid_index_raises(temp_history_file):
    history = CalculatorHistory(temp_history_file)
    with pytest.raises(IndexError):
        history.remove_calculation(5)

def test_load_from_existing_file(temp_history_file):
    with open(temp_history_file, "w") as f:
        f.write("num1,num2,operation,result\n1,2,add,3\n")
    history = CalculatorHistory(temp_history_file)
    assert len(history.list_calculations()) == 1
    assert history.list_calculations()[0]["operation"] == "add"
