# Makefile for euromillions-ga

VENV = .venv
PYTHON = uv run -- python -m euromillions

.PHONY: clean install fetch generate generate-data test

clean:
	rm -rf data/*.parquet
	find . -type d -name "__pycache__" -exec rm -rf {} +

install:
	uv pip install -e .
	uv pip install typer pandas pyarrow fastparquet rich

fetch:
	$(PYTHON) fetch-draws

generate:
	$(PYTHON) generate

generate-data: fetch generate

test:
	uv run -- pytest tests/
