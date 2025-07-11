# src/euromillions/generators/strategy_registry.py

from typing import Callable, Dict, Any, Tuple

from euromillions.generators.strategies.modulo_increment import generate_modulo_increment

# List of (strategy_function, params) to be genome-indexed
strategy_variants: list[Tuple[Callable, Dict[str, Any]]] = [
    (generate_modulo_increment, {"start": 1, "increment": 2}),
    (generate_modulo_increment, {"start": 3, "increment": 5}),
    (generate_modulo_increment, {"start": 7, "increment": 4}),
    (generate_modulo_increment, {"start": 10, "increment": 1}),
    (generate_modulo_increment, {"start": 2, "increment": 6}),
]

def get_strategy_variant(index: int) -> Tuple[Callable, Dict[str, Any]]:
    try:
        return strategy_variants[index]
    except IndexError:
        raise ValueError(f"Strategy index {index} out of range (max {len(strategy_variants) - 1})")
