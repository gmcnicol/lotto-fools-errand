"""
Collects all available ticket‐generation strategies.
"""

from typing import Callable, List, Tuple
import pandas as pd

# import your new strategies
from euromillions.generators.strategies import frequency_weighted_generator

# map names to callables
STRATEGIES: dict[str, Callable[[pd.DataFrame], Tuple[List[int], List[int]]]] = {
    "frequency_weighted": frequency_weighted_generator,
}

def get_all_strategy_variants() -> List[Callable[[pd.DataFrame], Tuple[List[int], List[int]]]]:
    """
    Return list of all strategy functions, in a fixed order.
    """
    return list(STRATEGIES.values())

def generate_tickets_from_variants(
        chromosome:  list[int],
        variants:    List[Callable[[pd.DataFrame], Tuple[List[int], List[int]]]],
        draws_df:    pd.DataFrame,
        max_tickets: int
) -> List[Tuple[List[int], List[int]]]:
    """
    For each gene==1 in `chromosome`, call the corresponding strategy
    (passing it the full `draws_df`), collect up to `max_tickets`.
    """
    tickets: List[Tuple[List[int], List[int]]] = []
    for gene, strat in zip(chromosome, variants):
        if gene:
            nums, stars = strat(draws_df)  # uses default num_numbers=5,num_stars=2
            tickets.append((nums, stars))
            if len(tickets) >= max_tickets:
                break
    return tickets
