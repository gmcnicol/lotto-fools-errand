import typer
import pandas as pd
from euromillions.euromillions_loader import fetch_and_cache_draws, load_draws_df
from euromillions.genetics.evolve import run_evolution

app = typer.Typer()

@app.command("fetch-draws")
def fetch_draws_command():
    fetch_and_cache_draws()
    print("Draws fetched and cached.")

@app.command("generate")
def generate_command():
    """
    Run the full genetic algorithm evolution and print the best chromosome and its tickets.
    """
    run_evolution()

@app.command("stats")
def stats_command():
    draws_df = load_draws_df()
    if draws_df.empty:
        print("No draws found.")
        return

    latest = pd.to_datetime(draws_df["date"]).max()
    earliest = pd.to_datetime(draws_df["date"]).min()
    total = len(draws_df)
    winners = draws_df["has_winner"].sum()
    prize_tiers = pd.json_normalize(draws_df["prizes"]).dropna().shape[0]

    print(f"Latest draw date: {latest.date()}")
    print(f"Earliest draw date: {earliest.date()}")
    print(f"Total draws: {total}")
    print(f"Winning draws: {winners}")
    print(f"Prize tiers (total across all draws): {prize_tiers}")

if __name__ == "__main__":
    app()
