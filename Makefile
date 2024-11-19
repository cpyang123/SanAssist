install:
	pip install -r requirements.txt

test:
	find ./src/tests -name "*test*.py" -exec python -m pytest --nbval -v {} +
	
lint:
	ruff check
pylint:
	find ./src/main_workspace -name "*.py" -exec pylint --disable=R,C {} +
format:
	find ./src/main_workspace -name "*.py" -exec black {} +
	find ./src/tests -name "*.py" -exec black {} +

all: install test lint format
