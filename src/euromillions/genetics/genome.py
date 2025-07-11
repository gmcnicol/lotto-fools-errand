from typing import List

from euromillions.generators.strategy_registry import get_strategy_variant
from euromillions.genetics.dedup import round_robin_dedup
from euromillions.genetics.fitness import evaluate_ticket_set_fitness
from euromillions.euromillions_loader import load_draws_df


def run_genome(
        genome: List[int],
        draws_df=None,
        num_tickets: int = 10,
        step: int = 3,
        window: int = 100,
):
    """
    Run a genome, generating and evaluating tickets.
    Each bit in the genome determines whether to activate a strategy variant.
    """
    if draws_df is None:
        draws_df = load_draws_df()

    active_strategies = [
        get_strategy_variant(i) for i, bit in enumerate(genome) if bit == 1
    ]

    if not active_strategies:
        raise ValueError("Genome did not activate any strategy variants.")

    # Generate tickets from each strategy
    all_ticket_sets = []
    for generator_fn, params in active_strategies:
        tickets = generator_fn(draws_df, step=step, window=window, **params)
        all_ticket_sets.append(tickets)

    # Combine tickets from all strategies
    combined = round_robin_dedup(all_ticket_sets, max_len=num_tickets)

    # Evaluate tickets against actual draws
    score, detail = evaluate_ticket_set_fitness(combined, draws_df)

    return {
        "genome": genome,
        "score": score,
        "tickets": combined,
        "detail": detail,
    }
