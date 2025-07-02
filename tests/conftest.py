from decimal import Decimal
import pytest
from faker import Faker
from app.operations import add, subtract, multiply, divide
import os
import tempfile

fake = Faker()

def generate_test_data(num_records):
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        if operation_func == divide and b == 0:
            b = Decimal('1')

        try:
            expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_func, expected  # Yield operation_func, not operation_name

def pytest_addoption(parser):
    parser.addoption("--num_records", action="store", default=5, type=int)

def pytest_generate_tests(metafunc):
    if {"a", "b", "operation", "expected"}.issubset(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        metafunc.parametrize("a,b,operation,expected", parameters)

@pytest.fixture(autouse=True, scope="session")
def set_history_file_env():
    # Create a temporary file for HISTORY_FILE environment variable
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    os.environ["HISTORY_FILE"] = temp_file.name
    yield
    # Cleanup after tests run
    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass
