# src/euromillions/generators/strategies/markov_chain.py

import random
from collections import Counter
from typing import List, Tuple, Callable
import pandas as pd

# A single ticket: (five numbers, two stars)
Ticket = Tuple[List[int], List[int]]
# Signature for one‑ticket‐list generator
Generator = Callable[[pd.DataFrame, int], List[Ticket]]


def get_variants(
        window_sizes: List[int] = [5, 10, 20],
        pseudocount: float = 1.0
) -> List[Generator]:
    """
    For each window size W, build a first‑order Markov chain over the last W+1 draws.
    Each variant returns a LIST of `count` tickets.
    """
    variants: List[Generator] = []

    for W in window_sizes:
        def make_generator(window: int):
            def generator(history: pd.DataFrame, count: int) -> List[Ticket]:
                tickets: List[Ticket] = []

                for _ in range(count):
                    # If not enough history, pick uniformly at random
                    if len(history) < 2:
                        nums = random.sample(range(1, 51), 5)
                        stars = random.sample(range(1, 13), 2)
                        tickets.append((nums, stars))
                        continue

                    # Only use the last window+1 draws to build the chain
                    df_w = (history
                            if len(history) <= window + 1
                            else history.iloc[-(window + 1):])

                    # Build transition counts: from draw_i → draw_{i+1}
                    trans: dict[int, Counter] = {i: Counter() for i in range(1, 51)}
                    num_lists = df_w["numbers"].tolist()
                    for prev_draw, next_draw in zip(num_lists, num_lists[1:]):
                        for x in prev_draw:
                            for y in next_draw:
                                trans[int(x)][int(y)] += 1

                    # Seed with one number from the very last draw
                    last_nums = history.iloc[-1]["numbers"]
                    seed = random.choice(last_nums)
                    picked = [int(seed)]
                    pool = set(range(1, 51)) - set(picked)

                    # Walk the chain to pick 4 more numbers
                    for _ in range(4):
                        candidates = list(pool)
                        weights = [
                            trans[picked[-1]].get(num, 0) + pseudocount
                            for num in candidates
                        ]
                        if sum(weights) <= 0:
                            nxt = random.choice(candidates)
                        else:
                            nxt = random.choices(candidates, weights, k=1)[0]
                        picked.append(nxt)
                        pool.remove(nxt)

                    # Stars remain uniform for now
                    stars = random.sample(range(1, 13), 2)
                    tickets.append((picked, stars))

                return tickets

            generator.__name__ = f"markov_chain_W{window}"
            return generator

        variants.append(make_generator(W))

    return variants
