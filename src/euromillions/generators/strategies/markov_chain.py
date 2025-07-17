# src/euromillions/generators/strategies/markov_chain.py

import random
from collections import Counter
from typing import List, Tuple, Callable, Optional
import pandas as pd

# A single ticket: (five numbers, two stars)
Ticket = Tuple[List[int], List[int]]
# Signature for ticket generators matching the other strategies
Generator = Callable[[pd.DataFrame, int], List[Ticket]]


def markov_chain_generator_factory(
        window_sizes: Optional[List[int]] = None,
        pseudocount: float = 1.0
) -> List[Generator]:
    """
    For each window size W, build a first‑order Markov chain over the last W+1 draws.
    Seed the next ticket with one number from the most recent draw, then
    “walk” through the chain to pick 4 more numbers.
    Stars are still chosen uniformly at random.
    """
    variants: List[Generator] = []
    # avoid mutable default
    if window_sizes is None:
        window_sizes = [5, 10, 20]

    for W in window_sizes:
        def make_generator(window: int):
            def generator(history: pd.DataFrame, max_tickets: int) -> List[Ticket]:
                """Generate up to ``max_tickets`` using a simple Markov chain."""
                tickets: List[Ticket] = []
                # Need at least two draws to build transitions
                if len(history) < 2:
                    for _ in range(max_tickets):
                        nums = random.sample(range(1, 51), 5)
                        stars = random.sample(range(1, 13), 2)
                        tickets.append((nums, stars))
                    return tickets

                # Only last window+1 draws
                df_w = history if len(history) <= window + 1 else history.iloc[-(window + 1):]

                # Build transition counts: from draw_i → draw_{i+1}
                trans: dict[int, Counter] = {i: Counter() for i in range(1, 51)}
                num_lists = df_w["numbers"].tolist()
                for prev, curr in zip(num_lists, num_lists[1:]):
                    for x in prev:
                        for y in curr:
                            trans[int(x)][int(y)] += 1

                last_nums = history.iloc[-1]["numbers"]
                for _ in range(max_tickets):
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

                    stars = random.sample(range(1, 13), 2)
                    tickets.append((picked, stars))

                return tickets

            generator.__name__ = f"markov_chain_W{window}"
            return generator

        variants.append(make_generator(W))

    return variants


# alias for registry
get_variants = markov_chain_generator_factory
