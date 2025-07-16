import random
from collections import Counter
import pandas as pd

WINDOW_SIZES = [5, 15, 30]
EXPONENTS    = [0.5, 1.0, 2.0]

def frequency_weighted_generator_factory(window_size: int, exponent: float):
    def generator(draws_df: pd.DataFrame, num_tickets: int):
        df = draws_df.iloc[-window_size:] if window_size and len(draws_df) > window_size else draws_df

        num_counts, star_counts = Counter(), Counter()
        for _, row in df.iterrows():
            for n in row["numbers"]:
                num_counts[int(n)] += 1
            for s in row["stars"]:
                star_counts[int(s)] += 1

        numbers = list(range(1, 51))
        stars   = list(range(1, 13))

        num_weights  = [(num_counts[n] ** exponent) + 1 for n in numbers]
        star_weights = [(star_counts[s] ** exponent) + 1 for s in stars]

        tickets = []
        for _ in range(num_tickets):
            picked_nums = set()
            while len(picked_nums) < 5:
                picked_nums.add(random.choices(numbers, weights=num_weights, k=1)[0])
            picked_stars = set()
            while len(picked_stars) < 2:
                picked_stars.add(random.choices(stars, weights=star_weights, k=1)[0])

            tickets.append((sorted(picked_nums), sorted(picked_stars)))

        return tickets

    generator.__name__ = f"freq_w{window_size}_exp{exponent}"
    return generator

def get_variants() -> list[callable]:
    variants = []
    for w in WINDOW_SIZES:
        for e in EXPONENTS:
            variants.append(frequency_weighted_generator_factory(w, e))
    print(f"Generated {len(variants)} frequency-weighted variants with window sizes {WINDOW_SIZES} and exponents {EXPONENTS}.")
    return variants
