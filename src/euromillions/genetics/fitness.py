# src/euromillions/genetics/fitness.py

from euromillions.generators.strategy_registry import get_strategy_variant
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

TICKET_COST = 2.5

def evaluate_genome(genome):
    """
    Given a binary genome, evaluate the total profit/loss using actual prize payouts.
    """
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    # Get only enabled strategy variants
    active_variants = [get_strategy_variant(i) for i, bit in enumerate(genome) if bit == 1]

    if not active_variants:
        return float('-inf')  # Penalize empty genomes

    tickets = generate_tickets_from_variants(draws_df, active_variants)
    total_cost = len(tickets) * TICKET_COST
    total_payout = 0

    for draw in draws_df.itertuples():
        draw_id = draw.draw_id
        prize_info = prizes_df.get(draw_id, {})
        for ticket in tickets:
            main, stars = ticket
            main_match = match_count(main, draw.main_numbers)
            star_match = match_count(stars, draw.lucky_stars)
            match_key = f"{main_match}+{star_match}"
            total_payout += prize_info.get(match_key, 0)

    return total_payout - total_cost

def match_count(a, b):
    return len(set(a) & set(b))
