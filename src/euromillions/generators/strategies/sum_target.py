import random
import pandas as pd


def sum_target_generator_factory(tolerance: float = 1.0):
    """Bias selections toward sums near the historical average."""

    def generator(draws_df: pd.DataFrame, num_tickets: int):
        sums = draws_df["numbers"].apply(lambda ns: sum(int(n) for n in ns))
        mean = sums.mean()
        std = sums.std() if sums.std() > 0 else 1

        numbers = list(range(1, 51))
        tickets = []
        for _ in range(num_tickets):
            for _ in range(1000):
                nums = sorted(random.sample(numbers, 5))
                s = sum(nums)
                if abs(s - mean) <= tolerance * std:
                    stars = random.sample(range(1, 13), 2)
                    tickets.append((nums, sorted(stars)))
                    break
            else:
                tickets.append((sorted(random.sample(numbers, 5)), sorted(random.sample(range(1, 13), 2))))
        return tickets

    generator.__name__ = f"sum_target_{tolerance}".replace(".", "_")
    return generator


def get_variants() -> list[callable]:
    return [sum_target_generator_factory(t) for t in [0.5, 1.0]]
