import random
import pandas as pd


def parity_balance_generator(draws_df: pd.DataFrame, num_tickets: int):
    """Generate tickets matching the most common even/odd split."""
    even_counts = draws_df["numbers"].apply(lambda ns: sum(1 for n in ns if int(n) % 2 == 0))
    target_even = int(even_counts.mode()[0]) if not even_counts.empty else 2

    evens = [n for n in range(1, 51) if n % 2 == 0]
    odds = [n for n in range(1, 51) if n % 2 == 1]

    tickets = []
    for _ in range(num_tickets):
        nums = random.sample(evens, target_even) + random.sample(odds, 5 - target_even)
        stars = random.sample(range(1, 13), 2)
        tickets.append((sorted(nums), sorted(stars)))
    return tickets


def get_variants() -> list[callable]:
    return [parity_balance_generator]
