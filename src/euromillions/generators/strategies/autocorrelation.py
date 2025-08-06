import random
from typing import List, Tuple, Callable

import numpy as np
import pandas as pd

Ticket = Tuple[List[int], List[int]]
Generator = Callable[[pd.DataFrame, int], List[Ticket]]

WINDOW_SIZES = [20, 50, 100]
LAGS = [1, 2, 3, 4, 5]

def _partial_autocorr(x: np.ndarray, lag: int) -> float:
    """Compute a simple partial autocorrelation for given lag.

    Uses Yule-Walker equations for AR(lag) model.
    Returns 0.0 if computation fails.
    """
    n = len(x)
    if lag >= n:
        return 0.0
    # autocorrelations for lags 0..lag
    acf = [1.0]
    for l in range(1, lag + 1):
        if l >= n:
            acf.append(0.0)
        else:
            val = pd.Series(x).autocorr(lag=l)
            acf.append(0.0 if pd.isna(val) else val)
    R = np.array([[acf[abs(i - j)] for j in range(lag)] for i in range(lag)])
    r = np.array(acf[1:lag + 1])
    try:
        phi = np.linalg.solve(R, r)
        val = float(phi[-1])
        return 0.0 if np.isnan(val) else val
    except np.linalg.LinAlgError:
        return 0.0

def _weights_for_balls(draw_series: pd.Series, balls: List[int], lag: int) -> List[float]:
    arr = np.zeros((len(draw_series), len(balls)), dtype=int)
    for idx, row in enumerate(draw_series):
        for n in row:
            arr[idx, int(n) - 1] = 1
    weights: List[float] = []
    for col in arr.T:
        if lag < len(col):
            ac_val = pd.Series(col).autocorr(lag=lag)
            acf = 0.0 if pd.isna(ac_val) else ac_val
            pacf = _partial_autocorr(col, lag)
            pacf = 0.0 if pd.isna(pacf) else pacf
            w = max(acf + pacf, 0.0) + 1.0
        else:
            w = 1.0
        weights.append(w)
    return weights

def autocorr_generator_factory(window: int, lag: int) -> Generator:
    def generator(draws_df: pd.DataFrame, max_tickets: int) -> List[Ticket]:
        df = draws_df.tail(window) if window and len(draws_df) > window else draws_df
        numbers = list(range(1, 51))
        stars = list(range(1, 13))
        num_weights = _weights_for_balls(df["numbers"], numbers, lag)
        star_weights = _weights_for_balls(df["stars"], stars, lag)
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
    generator.__name__ = f"autocorr_w{window}_lag{lag}"
    return generator

def get_variants() -> List[Generator]:
    variants: List[Generator] = []
    for w in WINDOW_SIZES:
        for l in LAGS:
            variants.append(autocorr_generator_factory(w, l))
    return variants
