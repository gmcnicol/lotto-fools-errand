# src/euromillions/genetics/fitness.py

from typing import List, Tuple
import pandas as pd
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Ticket = Tuple[List[int], List[int]]

TICKET_COST = 2.50  # GBP per ticket

def evaluate_ticket_set_fitness(tickets: List[Ticket], target_draw_id: int) -> float:
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    draw = draws_df[draws_df["draw_id"] == target_draw_id]
    if draw.empty:
        raise ValueError(f"No draw found for draw_id={target_draw_id}")
    draw = draw.iloc[0]

    winning_main = set(draw["main_numbers"])
    winning_stars = set(draw["lucky_stars"])

    prize_row = prizes_df[prizes_df["draw_id"] == target_draw_id]
    if prize_row.empty:
        raise ValueError(f"No prize breakdown found for draw_id={target_draw_id}")
    prize_row = prize_row.iloc[0]

    total_winnings = 0.0
    for main, stars in tickets:
        matched_main = len(set(main) & winning_main)
        matched_stars = len(set(stars) & winning_stars)
        prize_key = f"{matched_main}+{matched_stars}"

        prize = prize_row.get(prize_key, 0.0)
        if isinstance(prize, str):
            try:
                prize = float(prize.replace(",", ""))
            except ValueError:
                prize = 0.0
        total_winnings += prize

    cost = len(tickets) * TICKET_COST
    profit = total_winnings - cost
    return profit
