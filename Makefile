.PHONY: install clean fetch-draws generate stats

install:
	uv pip install -r requirements.txt

clean:
	find . -name '__pycache__' -exec rm -r {} +
	rm -f data/*.json data/*.parquet

fetch-draws:
	uv run -- python -m euromillions fetch-draws

generate:
	uv run -- python -m euromillions generate

stats:
	uv run -- python -m euromillions stats
