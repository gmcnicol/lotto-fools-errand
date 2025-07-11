# src/euromillions/generators/strategies/modulo_increment.py

import random
from typing import List, Tuple

def generate_modulo_increment(
        draws_df,
        step: int = 1,
        window: int = 100,
        modulus: int = 5,
        increment: int = 1,
        offset: int = 0,
) -> List[Tuple[List[int], List[int]]]:
    """
    Generate 10 tickets using modulo arithmetic on number space.
    Main numbers follow a modular pattern, stars are chosen randomly.

    Parameters:
        draws_df (DataFrame): Historical draws.
        step (int): Ignored in this strategy.
        window (int): Ignored in this strategy.
        modulus (int): Modulo base to define groups.
        increment (int): Step size for iterating candidates.
        offset (int): Offset for modular group starting point.

    Returns:
        List of 10 tickets, each a tuple of (main_numbers, lucky_stars)
    """
    available_main = list(range(1, 51))
    available_stars = list(range(1, 13))

    selected_main = []
    for i in range(offset, 50, increment):
        if i % modulus == offset:
            selected_main.append(i + 1)
        if len(selected_main) >= 5:
            break

    tickets = []
    for _ in range(10):
        main = sorted(random.sample(selected_main, 5))
        stars = sorted(random.sample(available_stars, 2))
        tickets.append((main, stars))

    return tickets
