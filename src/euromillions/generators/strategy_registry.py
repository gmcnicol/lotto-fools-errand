import pandas as pd
from typing import Callable

from euromillions.generators.strategies.modulo_increment import generate_modulo_increment


def get_all_strategy_variants():
    variants = []
    for start in range(1, 51):  # start: 1 to 50
        for increment in range(1, 11):  # increment: 1 to 10
            variants.append((generate_modulo_increment, {'start': start, 'increment': increment}))
    return variants


def generate_tickets_from_variants(
        chromosome: list[int],
        variants: list[tuple[Callable, dict]],
        draws_df: pd.DataFrame,
        max_tickets: int
) -> list[tuple[list[int], list[int]]]:
    """
    Uses active strategy variants (selected by chromosome) to generate up to `max_tickets` tickets.

    Returns a list of tickets: (numbers, stars)
    """
    active = [i for i, bit in enumerate(chromosome) if bit == 1]
    tickets = []

    for idx in active:
        strategy_func, kwargs = variants[idx]
        generated = strategy_func(draws_df=draws_df, **kwargs)
        tickets.extend(generated)
        if len(tickets) >= max_tickets:
            break

    return tickets[:max_tickets]
