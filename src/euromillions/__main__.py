import typer
from euromillions.euromillions_loader import fetch_and_cache_draws
from euromillions.genetics.evaluate_all_genomes import run_all_genomes

app = typer.Typer()

@app.command("fetch-draws")
def fetch_draws_command():
    fetch_and_cache_draws()
    print("Draws fetched and cached.")

@app.command("generate")
def generate_command():
    run_all_genomes()

if __name__ == "__main__":
    app()
