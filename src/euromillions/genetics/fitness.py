# src/euromillions/evolution/fitness.py

import pandas as pd
from typing import List
from euromillions.euromillions_loader import load_draws
from euromillions.generators.strategy_example import generate_strategy_example

TICKET_COST = 2.5  # £ per ticket

def compute_winnings(ticket_main: List[int], ticket_stars: List[int], draw: dict) -> float:
    matched_main = len(set(ticket_main) & set(draw["main_numbers"]))
    matched_stars = len(set(ticket_stars) & set(draw["lucky_stars"]))

    key = f"{matched_main}+{matched_stars}"
    breakdown = draw.get("prize_breakdown", {})

    prize = breakdown.get(key, {}).get("prize", 0.0)
    return float(prize)

def evaluate_genome(genome: List[int], draws_df: pd.DataFrame, step: int = 3, window: int = 100) -> float:
    profit = 0.0
    cost = 0.0

    for i in range(window, len(draws_df) - 1, step):
        train_draws = draws_df.iloc[i - window:i]
        next_draw = draws_df.iloc[i + 1]

        # For now, only use strategy_example (genome ignored)
        tickets = generate_strategy_example(train_draws)

        for ticket in tickets:
            main, stars = ticket
            winnings = compute_winnings(main, stars, next_draw)
            profit += winnings
            cost += TICKET_COST

    return profit - cost
