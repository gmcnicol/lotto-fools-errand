import pandas as pd
import random
from typing import Tuple, List

def frequency_weighted_generator(
        draws_df: pd.DataFrame,
        num_numbers: int = 5,
        num_stars:   int = 2
) -> Tuple[List[int], List[int]]:
    """
    Pick `num_numbers` out of 1–50 and `num_stars` out of 1–12,
    weighted by how often each has appeared in draws_df.
    """

    # flatten past numbers & stars into lists
    all_nums  = [n for row in draws_df["numbers"] for n in map(int, row)]
    all_stars = [s for row in draws_df["stars"]   for s in map(int, row)]

    # count occurrences
    num_counts  = pd.Series(all_nums).value_counts().to_dict()
    star_counts = pd.Series(all_stars).value_counts().to_dict()

    # build pools and weights (+1 so nothing has zero weight)
    num_pool     = list(range(1, 51))
    num_weights  = [num_counts.get(i, 0) + 1 for i in num_pool]

    star_pool    = list(range(1, 13))
    star_weights = [star_counts.get(i, 0) + 1 for i in star_pool]

    def weighted_sample(pool, weights, k):
        pool, weights = pool[:], weights[:]
        picks: List[int] = []
        for _ in range(k):
            choice = random.choices(pool, weights=weights, k=1)[0]
            idx = pool.index(choice)
            picks.append(choice)
            pool.pop(idx)
            weights.pop(idx)
        return sorted(picks)

    numbers = weighted_sample(num_pool, num_weights, num_numbers)
    stars   = weighted_sample(star_pool, star_weights, num_stars)

    return numbers, stars
