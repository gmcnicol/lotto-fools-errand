from typing import List, Tuple, Any
from pandas import DataFrame

def generate_tickets_from_variants(
        draws_df: DataFrame,
        variants: List[Tuple],
        max_tickets: int = 7
) -> List[Any]:
    all_tickets = []
    for func, params in variants:
        tickets = func(draws_df=draws_df, **params)
        all_tickets.extend(tickets)
        if len(all_tickets) >= max_tickets:
            break

    return all_tickets[:max_tickets]
