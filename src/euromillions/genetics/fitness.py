# src/euromillions/genetics/fitness.py

from typing import List, Tuple
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Ticket = Tuple[List[int], List[int]]

def evaluate_ticket_set(
        tickets: List[Ticket],
        draws_df,
        prizes_df
) -> float:
    total_cost = len(tickets) * 2.5
    total_winnings = 0

    for _, draw in draws_df.iterrows():
        draw_id = draw["draw_id"]
        prize_breakdown = prizes_df.get(draw_id, {})

        for main, stars in tickets:
            main_matches = len(set(main) & set(draw["main_numbers"]))
            star_matches = len(set(stars) & set(draw["lucky_stars"]))

            key = f"{main_matches}+{star_matches}"
            prize = prize_breakdown.get(key, 0)
            total_winnings += prize

    return total_winnings - total_cost
