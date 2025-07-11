from typing import Callable, List, Tuple
import pandas as pd

Ticket = Tuple[List[int], List[int]]

def generate_tickets_from_variants(
        draws_df: pd.DataFrame,
        variants: List[Tuple[Callable, dict]]
) -> List[Ticket]:
    all_tickets = []
    for func, params in variants:
        tickets = func(draws_df=draws_df, **params)
        all_tickets.extend(tickets)
    return all_tickets
