# src/euromillions/genetics/genome.py

from typing import List, Tuple

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import get_strategy_variant
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.genetics.fitness import evaluate_ticket_set

Ticket = Tuple[List[int], List[int]]

def round_robin_dedup(tickets: List[Ticket], count: int) -> List[Ticket]:
    seen = set()
    result = []
    for main, stars in tickets:
        key = (tuple(sorted(main)), tuple(sorted(stars)))
        if key not in seen:
            seen.add(key)
            result.append((main, stars))
        if len(result) >= count:
            break
    return result

def run_genome(
        genome: List[int],
        draws_df = None,
        prizes_df = None,
        num_tickets: int = 10
):
    if draws_df is None:
        draws_df = load_draws_df()
    if prizes_df is None:
        prizes_df = load_prizes_df()

    # Activate strategy variants
    active_variants = [
        get_strategy_variant(i)
        for i, bit in enumerate(genome)
        if bit == 1
    ]

    tickets = generate_tickets_from_variants(draws_df, active_variants)
    tickets = round_robin_dedup(tickets, num_tickets)

    score = evaluate_ticket_set(tickets, draws_df, prizes_df)
    return {
        "genome": genome,
        "tickets": tickets,
        "score": score
    }
