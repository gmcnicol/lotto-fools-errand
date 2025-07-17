import random
from collections import Counter
import pandas as pd


def pair_frequency_generator_factory(window: int | None = None):
    """Weight choices by historical pair frequencies."""

    def generator(draws_df: pd.DataFrame, num_tickets: int):
        df = draws_df if window is None else draws_df.tail(window)

        pair_counts: Counter[frozenset[int]] = Counter()
        base_counts: Counter[int] = Counter()

        for _, row in df.iterrows():
            nums = [int(n) for n in row["numbers"]]
            base_counts.update(nums)
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    pair = frozenset({nums[i], nums[j]})
                    pair_counts[pair] += 1

        numbers = list(range(1, 51))

        tickets = []
        for _ in range(num_tickets):
            picked = set()
            weights = [base_counts[n] + 1 for n in numbers]
            first = random.choices(numbers, weights=weights, k=1)[0]
            picked.add(first)

            while len(picked) < 5:
                candidates = [n for n in numbers if n not in picked]
                cand_w = []
                for n in candidates:
                    w = 1
                    for p in picked:
                        w += pair_counts[frozenset({n, p})]
                    cand_w.append(w)
                nxt = random.choices(candidates, weights=cand_w, k=1)[0]
                picked.add(nxt)

            stars = random.sample(range(1, 13), 2)
            tickets.append((sorted(picked), sorted(stars)))
        return tickets

    w_name = "all" if window is None else str(window)
    generator.__name__ = f"pair_freq_w{w_name}"
    return generator


def get_variants() -> list[callable]:
    windows = [None, 30]
    return [pair_frequency_generator_factory(w) for w in windows]
