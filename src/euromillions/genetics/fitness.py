import pandas as pd
import logging

logger = logging.getLogger(__name__)


def evaluate_ticket_set(
        tickets: list[tuple[list[int], list[int]]],
        draws_df: pd.DataFrame,
        prizes_df: pd.DataFrame
) -> float:
    score = 0.0

    for _, row in draws_df.iterrows():
        draw_numbers = set(row["numbers"])
        draw_stars = set(row["stars"])

        for ticket_numbers, ticket_stars in tickets:
            matched_numbers = len(draw_numbers & set(ticket_numbers))
            matched_stars = len(draw_stars & set(ticket_stars))

            # Look up matching prize in prizes_df
            prize_row = prizes_df[
                (prizes_df["matched_numbers"] == matched_numbers) &
                (prizes_df["matched_stars"] == matched_stars)
                ]
            if not prize_row.empty:
                prize = prize_row.iloc[0].get("prize_gbp", 0.0)
                logger.info(
                    f"Ticket {ticket_numbers}+{ticket_stars}: matched {matched_numbers} numbers, "
                    f"{matched_stars} stars, prize {prize}"
                )
                score += prize
            else:
                logger.info(
                    f"Ticket {ticket_numbers}+{ticket_stars}: matched {matched_numbers} numbers, "
                    f"{matched_stars} stars, no prize"
                )

    total_cost = len(tickets) * 2.5 * len(draws_df)
    logger.info(f"Total score: {score}, total cost: {total_cost}, net: {score - total_cost}")
    return score - total_cost
