from typing import List, Tuple
import pandas as pd

Ticket = Tuple[List[int], List[int]]

def generate_strategy_example(draws_df: pd.DataFrame, step: int = 3, window: int = 100) -> List[Ticket]:
    """
    Deterministic strategy: shifts past draw numbers using modular arithmetic.
    Returns a list of 10 valid EuroMillions tickets.
    """
    recent_draws = draws_df[-window:].reset_index(drop=True)
    result: List[Ticket] = []

    for i in range(10):
        index = (i * step) % len(recent_draws)
        draw = recent_draws.iloc[index]
        base_main = [int(n) for n in draw["main_numbers"]]
        base_star = [int(n) for n in draw["star_numbers"]]

        # Shift numbers in a repeatable pattern
        shifted_main = [(n + step + i) % 50 + 1 for n in base_main]
        shifted_star = [(s + step + i) % 12 + 1 for s in base_star]

        # Ensure unique, sorted, valid ticket
        main_numbers = sorted(list(dict.fromkeys(shifted_main)))[:5]
        star_numbers = sorted(list(dict.fromkeys(shifted_star)))[:2]

        result.append((main_numbers, star_numbers))

    return result
