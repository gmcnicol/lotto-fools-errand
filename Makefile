.PHONY: install fetch-draws generate stats clean

install:
	uv venv
	uv pip install -r requirements.txt

fetch-draws:
	uv run -- python -m euromillions fetch-draws

generate:
	uv run -- python -m euromillions generate

stats:
	uv run -- python -m euromillions stats

clean:
	rm -rf .venv __pycache__ .mypy_cache .pytest_cache dist build *.egg-info *.zip

zip:
	rm -f *.zip
	zip -r euromillions-ga-src.zip src Makefile pyproject.toml \
		-x '**/__pycache__/*' '**/*.pyc' '**/.DS_Store' '**/.mypy_cache/*' '**/.pytest_cache/*' 'Makefile'

unzip:
	@echo "Usage: make unzip FILE=name-of-zip.zip"
	@[ -z "$(FILE)" ] && echo "Missing FILE argument" && exit 1 || unzip -o $(FILE) -d .

