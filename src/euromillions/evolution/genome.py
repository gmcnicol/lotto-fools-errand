from typing import List, Dict, Callable, Tuple
from euromillions.generators import strategies
from euromillions.evolution import evaluator, fitness
from euromillions.evolution.combiners import round_robin_dedup
import pandas as pd


def get_strategies_from_genome(
        genome: List[int],
        strategy_funcs: Dict[str, Callable]
) -> Dict[str, Callable]:
    """
    Filters strategy functions by genome activation bits.
    """
    active = {}
    names = list(strategy_funcs.keys())
    for i, bit in enumerate(genome):
        if bit and i < len(names):
            name = names[i]
            active[name] = strategy_funcs[name]
    return active


def evaluate_genome(
        genome: List[int],
        draws_df: pd.DataFrame,
        window: int = 100,
        step: int = 3,
        verbose: bool = False
) -> List[Dict[str, int]]:
    """
    Runs draw-by-draw evolution using a genome to select strategies.
    Returns per-draw performance history.
    """
    results = []
    strategy_funcs = strategies.get_all_strategies()
    selected = get_strategies_from_genome(genome, strategy_funcs)

    if not selected:
        raise ValueError("Genome selected no strategies.")

    for i in range(1, len(draws_df)):
        history = draws_df.iloc[:i]
        target = draws_df.iloc[i]

        # Generate tickets from each strategy
        all_tickets = []
        for func in selected.values():
            all_tickets.extend(func(draws_df=history, step=step, window=window))

        # Combine into final ticket set
        combined = round_robin_dedup(all_tickets, limit=10)

        match_results = evaluator.evaluate_all_tickets(
            combined,
            draw_main=target["main_numbers"],
            draw_stars=target["star_numbers"]
        )

        score = fitness.score_all_tickets(match_results)

        if verbose:
            print(f"Draw {i+1}: Genome score {score}")

        results.append({
            "draw_number": i + 1,
            "genome": genome,
            "score": score
        })

    return results
