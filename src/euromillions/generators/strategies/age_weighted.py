import random
import pandas as pd


def age_weighted_generator_factory(exponent: float = 1.0):
    """Generate tickets giving more weight to numbers not drawn recently."""

    def generator(draws_df: pd.DataFrame, num_tickets: int):
        numbers = list(range(1, 51))
        stars = list(range(1, 13))

        age_nums = {n: len(draws_df) for n in numbers}
        age_stars = {s: len(draws_df) for s in stars}
        seen_nums: set[int] = set()
        seen_stars: set[int] = set()

        for age, (_, row) in enumerate(draws_df.iloc[::-1].iterrows()):
            for n in row["numbers"]:
                n = int(n)
                if n not in seen_nums:
                    age_nums[n] = age
                    seen_nums.add(n)
            for s in row["stars"]:
                s = int(s)
                if s not in seen_stars:
                    age_stars[s] = age
                    seen_stars.add(s)
            if len(seen_nums) == 50 and len(seen_stars) == 12:
                break

        num_weights = [(age_nums[n] + 1) ** exponent for n in numbers]
        star_weights = [(age_stars[s] + 1) ** exponent for s in stars]

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

    generator.__name__ = f"age_weighted_exp{exponent}"
    return generator


def get_variants() -> list[callable]:
    exps = [1.0, 2.0]
    return [age_weighted_generator_factory(e) for e in exps]
