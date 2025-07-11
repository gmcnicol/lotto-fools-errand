import typer
from euromillions.euromillions_loader import fetch_and_cache_draws
from euromillions.genetics.evolve import run_genetic_algorithm

app = typer.Typer()

@app.command("fetch-draws")
def fetch_draws_command():
    fetch_and_cache_draws()
    print("Draws fetched and cached.")

@app.command("generate")
def generate_command():
    run_genetic_algorithm()

if __name__ == "__main__":
    app()
