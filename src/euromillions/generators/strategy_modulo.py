from typing import List, Tuple
import pandas as pd
from euromillions.types import Ticket

def generate_modulo_strategy(draws_df: pd.DataFrame, start: int, increment: int) -> List[Ticket]:
    tickets = []
    for i in range(5):
        numbers = [(start + i * increment + j) % 50 + 1 for j in range(5)]
        stars = [(start + i * increment + j) % 12 + 1 for j in range(2)]
        tickets.append((sorted(numbers), sorted(stars)))
    return tickets