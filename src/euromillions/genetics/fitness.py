import pandas as pd


def evaluate_ticket_set(tickets: list[tuple[list[int], list[int]]], draws_df: pd.DataFrame, prizes_df: pd.DataFrame) -> float:
    score = 0.0

    for _, row in draws_df.iterrows():
        draw_numbers = set(row["numbers"])
        draw_stars = set(row["stars"])

        for ticket_numbers, ticket_stars in tickets:  # ✅ FIXED unpack here
            matched_numbers = len(draw_numbers & set(ticket_numbers))
            matched_stars = len(draw_stars & set(ticket_stars))

            # Look up matching prize
            for prize in row["prizes"]:
                if (
                        prize["matched_numbers"] == matched_numbers
                        and prize["matched_stars"] == matched_stars
                ):
                    score += prize.get("prize_gbp", 0.0)

    total_cost = len(tickets) * 2.5 * len(draws_df)
    return score - total_cost
