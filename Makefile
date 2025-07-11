.PHONY: install clean generate-data generate evolve-genome

UV ?= uv
PYTHON := .venv/bin/python

install:
	$(UV) pip install -e .
	$(UV) pip install typer pandas pyarrow fastparquet rich

clean:
	rm -rf data/*.parquet
	find . -type d -name "__pycache__" -exec rm -rf {} +

generate-data:
	$(UV) run -- python -m euromillions fetch-draws

generate:
	$(UV) run -- python -m euromillions generate --strategy strategy_example --step 3 --window 100

evolve-genome:
	$(UV) run -- python -m euromillions evolve-genome --genome 1 --step 3 --window 100
