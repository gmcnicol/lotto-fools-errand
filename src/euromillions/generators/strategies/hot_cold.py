import pandas as pd
from collections import Counter

def get_variants(window_sizes=None):
    """
    Return a list of generator functions, one per window size.
    Each generator must accept (draws_df, max_tickets)
    and return a list of up to max_tickets (numbers, stars) tuples.
    """
    if window_sizes is None:
        window_sizes = [13, 21, 34, 55, 89, 144, 233]  # big Fibonacci numbers

    variants = []
    for w in window_sizes:
        variants.append(hot_cold_generator_factory(w))
    return variants


def hot_cold_generator_factory(window: int):
    """
    Build a generator that looks at the last `window` draws,
    counts frequency of each ball, then picks the hottest ones.
    """

    def generator(draws_df: pd.DataFrame, max_tickets: int):
        # we only need the last `window` draws
        recent = draws_df.tail(window)

        # count how often each number/stars appeared
        num_counts = Counter(n for row in recent["numbers"] for n in row)
        star_counts = Counter(s for row in recent["stars"]   for s in row)

        # sort balls by descending frequency
        hottest_nums = [n for n, _ in num_counts.most_common(5 * max_tickets)]
        hottest_stars = [s for s, _ in star_counts.most_common(2 * max_tickets)]

        tickets = []
        # emit up to max_tickets distinct tickets by slicing
        for i in range(max_tickets):
            nums = hottest_nums[i*5:(i+1)*5]
            stars = hottest_stars[i*2:(i+1)*2]
            if len(nums) == 5 and len(stars) == 2:
                tickets.append((nums, stars))
        return tickets

    return generator
