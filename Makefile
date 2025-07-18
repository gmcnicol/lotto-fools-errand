.PHONY: install fetch-draws generate stats clean generate-with-redirect zip unzip

install:
	uv venv
	uv pip install -r requirements.txt

fetch-draws:
	-uv run -- python -m euromillions fetch-draws

generate:
	uv run -- python -m euromillions generate

generate-with-redirect:
	-uv run -- python -m euromillions generate >out.txt 2>&1 || true
stats:
	uv run -- python -m euromillions stats

clean:
	rm -rf .venv __pycache__ .mypy_cache .pytest_cache dist build *.egg-info *.zip

zip:
	rm -f *.zip
	zip -r euromillions-ga-src.zip src Makefile pyproject.toml out.txt \
		-x '**/__pycache__/*' '**/*.pyc' '**/.DS_Store' '**/.mypy_cache/*' '**/.pytest_cache/*' 'Makefile' '**/.venv/*' 'dist/*' 'build/*' '*.egg-info/*'

unzip:
	@echo "Usage: make unzip FILE=name-of-zip.zip"
	@[ -z "$(FILE)" ] && echo "Missing FILE argument" && exit 1 || unzip -o $(FILE) -d .

all: clean install fetch-draws generate-with-redirect clean zip