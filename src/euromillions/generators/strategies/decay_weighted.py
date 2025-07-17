import random
import pandas as pd


def decay_weighted_generator_factory(decay: float = 0.95, window: int | None = None):
    """Exponential decay weighting of past draws."""

    def generator(draws_df: pd.DataFrame, num_tickets: int):
        df = draws_df if window is None else draws_df.tail(window)
        numbers = list(range(1, 51))
        stars = list(range(1, 13))

        num_scores = {n: 0.0 for n in numbers}
        star_scores = {s: 0.0 for s in stars}
        for age, (_, row) in enumerate(df.iloc[::-1].iterrows()):
            factor = decay ** age
            for n in row["numbers"]:
                num_scores[int(n)] += factor
            for s in row["stars"]:
                star_scores[int(s)] += factor

        num_weights = [num_scores[n] + 1e-6 for n in numbers]
        star_weights = [star_scores[s] + 1e-6 for s in stars]

        tickets = []
        for _ in range(num_tickets):
            nums = set()
            while len(nums) < 5:
                nums.add(random.choices(numbers, weights=num_weights, k=1)[0])
            stars_pick = set()
            while len(stars_pick) < 2:
                stars_pick.add(random.choices(stars, weights=star_weights, k=1)[0])
            tickets.append((sorted(nums), sorted(stars_pick)))
        return tickets

    w_name = "all" if window is None else str(window)
    generator.__name__ = f"decay{decay}_w{w_name}"
    return generator


def get_variants() -> list[callable]:
    decays = [0.9, 0.95]
    windows = [None, 20]
    return [decay_weighted_generator_factory(d, w) for d in decays for w in windows]
