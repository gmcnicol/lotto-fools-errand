# src/euromillions/__main__.py

import typer
from euromillions.euromillions_loader import fetch_and_cache_draws, load_draws_df
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.generators.strategy_registry import get_strategy_variant

app = typer.Typer()

@app.command("fetch-draws")
def fetch_draws_command():
    """
    Fetch EuroMillions draws from API and cache them.
    """
    fetch_and_cache_draws()
    typer.secho("Draws fetched and cached.", fg=typer.colors.GREEN)

@app.command("generate")
def generate_command(
        strategy_index: int = typer.Option(0, "--strategy-index", "-i", help="Index of strategy variant"),
        step: int = typer.Option(3, "--step", "-s"),
        window: int = typer.Option(100, "--window", "-w"),
):
    """
    Generate EuroMillions tickets using a specified strategy variant.
    """
    draws_df = load_draws_df()

    func, params = get_strategy_variant(strategy_index)
    params.update({"step": step, "window": window})

    tickets = generate_tickets_from_variants(draws_df=draws_df, variants=[(func, params)])

    typer.secho(f"Strategy Index: {strategy_index}", fg=typer.colors.BLUE)
    for i, (main, stars) in enumerate(tickets, 1):
        typer.echo(f"{i:2d}. Main: {main} | Stars: {stars}")

if __name__ == "__main__":
    app()
