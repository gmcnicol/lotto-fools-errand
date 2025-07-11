import random
import pandas as pd
from collections import Counter

MAIN_POOL = list(range(1, 51))
STAR_POOL = list(range(1, 13))

# === Shared utils ===
def pick_unique(pool, count):
    return sorted(random.sample(pool, count))

# === Strategy 1: Pure random ===
def generate_pure_random():
    return [(pick_unique(MAIN_POOL, 5), pick_unique(STAR_POOL, 2)) for _ in range(10)]

# === Strategy 2: Arithmetic sequence ===
def generate_arithmetic_seq(start=1, step=3):
    tickets = []
    for i in range(10):
        nums = [(start + step * n + i) % 50 + 1 for n in range(5)]
        stars = [(start + step * n + i) % 12 + 1 for n in range(2)]
        tickets.append((sorted(set(nums)[:5]), sorted(set(stars)[:2])))
    return tickets

# === Strategy 3: Frequency-biased ===
def generate_frequency_biased(draws_df, window=100):
    pool = draws_df.tail(window)
    
    num_counts = Counter()
    star_counts = Counter()
    for _, row in pool.iterrows():
        num_counts.update(row["numbers"])
        star_counts.update(row["stars"])
    
    num_weights = [num_counts.get(n, 1) for n in MAIN_POOL]
    star_weights = [star_counts.get(s, 1) for s in STAR_POOL]

    tickets = []
    for _ in range(10):
        nums = sorted(random.choices(MAIN_POOL, weights=num_weights, k=20))
        stars = sorted(random.choices(STAR_POOL, weights=star_weights, k=10))
        tickets.append((
            sorted(set(nums))[:5],
            sorted(set(stars))[:2]
        ))
    return tickets

# === Strategy Selector ===
def generate_tickets(strategy, draws_df=None, **kwargs):
    if strategy == "pure_random":
        return generate_pure_random()
    elif strategy == "arithmetic_seq":
        return generate_arithmetic_seq(**kwargs)
    elif strategy == "frequency_biased":
        return generate_frequency_biased(draws_df, **kwargs)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

# === Run standalone
if __name__ == "__main__":
    from euromillions_loader import load_draws
    df = load_draws()

    for strategy in ["pure_random", "arithmetic_seq", "frequency_biased"]:
        print(f"\n{strategy.upper()} TICKETS:\n")
        tickets = generate_tickets(strategy, draws_df=df, window=200, step=4)
        for main, stars in tickets:
            print(f"  Main: {main}  Stars: {stars}")
