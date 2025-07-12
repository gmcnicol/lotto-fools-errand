import pandas as pd
import logging

logger = logging.getLogger(__name__)

def evaluate_ticket_set(
        tickets: list[tuple[list[int], list[int]]],
        draws_df: pd.DataFrame,
        prizes_df: pd.DataFrame
) -> float:
    """
    Evaluate a set of tickets by simulating them against historical draws
    and summing up the returned prize amounts (minus ticket costs).
    """
    score = 0.0

    for _, row in draws_df.iterrows():
        draw_numbers = set(map(int, row["numbers"]))
        draw_stars = set(map(int, row["stars"]))
        prize_list = row.get("prizes", [])

        for ticket_numbers, ticket_stars in tickets:
            matched_numbers = len(draw_numbers.intersection(ticket_numbers))
            matched_stars = len(draw_stars.intersection(ticket_stars))

            # Find matching prize tier
            prize_info = next(
                (p for p in prize_list
                 if p.get("matched_numbers") == matched_numbers
                 and p.get("matched_stars") == matched_stars),
                None
            )

            if prize_info:
                prize_amount = prize_info.get("prize", 0.0)
                logger.debug(
                    f"Ticket {ticket_numbers}+{ticket_stars}: matched {matched_numbers} numbers, "
                    f"{matched_stars} stars, prize {prize_amount}"
                )
                score += prize_amount
            else:
                logger.debug(
                    f"Ticket {ticket_numbers}+{ticket_stars}: matched {matched_numbers} numbers, "
                    f"{matched_stars} stars, no prize"
                )

    # Subtract cost of tickets (EUR 2.50 per ticket per draw)
    total_cost = len(tickets) * 2.5 * len(draws_df)
    return score - total_cost
