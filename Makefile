.PHONY: fetch generate stats

fetch:
	uv run -- python -m euromillions fetch-draws

generate:
	uv run -- python -m euromillions generate

stats:
	uv run -- python -m euromillions stats
