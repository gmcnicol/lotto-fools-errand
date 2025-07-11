from typing import List, Tuple
import pandas as pd
from collections import defaultdict

Ticket = Tuple[List[int], List[int]]  # ([main numbers], [stars])

def evaluate_ticket_set(
        tickets: List[Ticket],
        draws_df: pd.DataFrame,
        prizes_df: pd.DataFrame
) -> float:
    """
    Evaluate a set of tickets against historical draws.
    Returns total profit or expected return.
    """
    total_payout = 0.0
    total_spent = len(tickets) * 2.50 * len(draws_df)  # £2.50 per ticket per draw

    for _, draw in draws_df.iterrows():
        draw_numbers = set(draw["numbers"])
        draw_stars = set(draw["stars"])
        draw_id = draw["draw_id"]

        # Get corresponding prize tier list
        prize_row = prizes_df.loc[prizes_df["draw_id"] == draw_id]
        if prize_row.empty:
            continue

        try:
            prize_tiers = prize_row.iloc[0]["prizes"]
        except (KeyError, IndexError):
            continue

        for ticket in tickets:
            main, stars = ticket
            matched_main = len(set(main) & draw_numbers)
            matched_stars = len(set(stars) & draw_stars)

            for tier in prize_tiers:
                if (tier["matched_numbers"], tier["matched_stars"]) == (matched_main, matched_stars):
                    total_payout += float(tier.get("prize", 0.0))
                    break

    net_return = total_payout - total_spent
    return net_return
