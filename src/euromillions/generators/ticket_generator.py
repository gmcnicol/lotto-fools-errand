from typing import Callable, Dict, List, Tuple
import random

def generate_tickets_from_variants(draws_df, selected_variants: List[Tuple[Callable, Dict]], max_tickets: int = 7):
    all_tickets = []
    for fn, params in selected_variants:
        # Explicitly pass draws_df to generators that expect it
        tickets = fn(draws_df=draws_df, **params)
        all_tickets.extend(tickets)
    random.shuffle(all_tickets)
    return all_tickets[:max_tickets]
