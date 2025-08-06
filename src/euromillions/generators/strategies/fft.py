import random
from typing import List, Tuple, Callable

import numpy as np
import pandas as pd

Ticket = Tuple[List[int], List[int]]
Generator = Callable[[pd.DataFrame, int], List[Ticket]]

WINDOW_SIZES = [20, 50, 100]
FREQ_INDICES = [1, 2, 3, 4, 5]

def _fft_amplitudes(draw_series: pd.Series, balls: List[int], freq_idx: int) -> List[float]:
    arr = np.zeros((len(draw_series), len(balls)))
    for i, row in enumerate(draw_series):
        for n in row:
            arr[i, int(n) - 1] = 1.0
    weights: List[float] = []
    for col in arr.T:
        fft_vals = np.fft.rfft(col)
        if freq_idx < len(fft_vals):
            amp = float(np.abs(fft_vals[freq_idx]))
            w = amp + 1.0
        else:
            w = 1.0
        weights.append(w)
    return weights

def fft_generator_factory(window: int, freq_idx: int) -> Generator:
    def generator(draws_df: pd.DataFrame, max_tickets: int) -> List[Ticket]:
        df = draws_df.tail(window) if window and len(draws_df) > window else draws_df
        numbers = list(range(1, 51))
        stars = list(range(1, 13))
        num_weights = _fft_amplitudes(df["numbers"], numbers, freq_idx)
        star_weights = _fft_amplitudes(df["stars"], stars, freq_idx)
        tickets: List[Ticket] = []
        for _ in range(max_tickets):
            picked_nums = set()
            while len(picked_nums) < 5:
                picked_nums.add(random.choices(numbers, weights=num_weights, k=1)[0])
            picked_stars = set()
            while len(picked_stars) < 2:
                picked_stars.add(random.choices(stars, weights=star_weights, k=1)[0])
            tickets.append((sorted(picked_nums), sorted(picked_stars)))
        return tickets
    generator.__name__ = f"fft_w{window}_f{freq_idx}"
    return generator

def get_variants() -> List[Generator]:
    variants: List[Generator] = []
    for w in WINDOW_SIZES:
        for f in FREQ_INDICES:
            variants.append(fft_generator_factory(w, f))
    return variants
