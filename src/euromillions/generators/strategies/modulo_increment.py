# src/euromillions/generators/strategies/modulo_increment.py

from typing import List, Tuple
import pandas as pd

Ticket = Tuple[List[int], List[int]]

def generate_modulo_increment(draws_df: pd.DataFrame, start: int = 1, increment: int = 1) -> List[Ticket]:
    """
    Strategy that generates a ticket by selecting numbers starting from `start` and incrementing by `increment`.
    Wraps around 50 for numbers and 12 for stars.

    Parameters:
        draws_df (pd.DataFrame): Not used directly, but included to match expected function signature.
        start (int): Starting number for sequence.
        increment (int): Increment step for sequence.

    Returns:
        List[Ticket]: A single ticket with 5 numbers and 2 stars.
    """

    numbers = [(start + i * increment - 1) % 50 + 1 for i in range(5)]
    stars = [(start + i * increment - 1) % 12 + 1 for i in range(2)]
    return [(numbers, stars)]
