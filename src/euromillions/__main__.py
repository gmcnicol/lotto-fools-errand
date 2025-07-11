# src/euromillions/__main__.py

import typer
from euromillions.euromillions_loader import load_draws, fetch_and_cache_draws
from euromillions.generators.ticket_generator import generate_tickets
from euromillions.evolution import genome as genome_runner

app = typer.Typer(help="🎰 EuroMillions CLI")

@app.command("fetch-draws")
def fetch_draws_command():
    """
    Fetch EuroMillions draws from API and cache them.
    """
    fetch_and_cache_draws()
    typer.secho("✅ Draws fetched and cached.", fg=typer.colors.GREEN)

@app.command("generate")
def generate_command(
        strategy: str = typer.Option(..., "--strategy", "-s"),
        step: int = typer.Option(3, "--step", "-t"),
        window: int = typer.Option(100, "--window", "-w")
):
    """
    Generate 10 EuroMillions tickets using a named strategy.
    """
    draws = load_draws()
    tickets = generate_tickets(strategy, draws_df=draws, step=step, window=window)

    typer.secho(f"\n🎟️  Strategy: {strategy}", fg=typer.colors.GREEN)
    for i, (main, stars) in enumerate(tickets, 1):
        typer.echo(f"{i:2d}. Main: {main} | Stars: {stars}")

@app.command("evolve-genome")
def evolve_genome_command(
        genome_str: str = typer.Option(..., "--genome", "-g", help="Binary genome like 0110101011"),
        step: int = typer.Option(3, "--step", "-t"),
        window: int = typer.Option(100, "--window", "-w"),
):
    """
    Evolve a genome over historical draws.
    """
    genome = [int(c) for c in genome_str.strip() if c in "01"]
    draws = load_draws()

    trace = genome_runner.evaluate_genome(
        genome=genome,
        draws_df=draws,
        window=window,
        step=step,
        verbose=True
    )

    typer.secho(f"\n🧬 Genome {genome} results:", fg=typer.colors.MAGENTA)
    for entry in trace:
        typer.echo(f"Draw {entry['draw_number']:>3}: score={entry['score']}")

if __name__ == "__main__":
    app()
