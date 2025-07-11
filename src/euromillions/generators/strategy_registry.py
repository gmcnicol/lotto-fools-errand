# src/euromillions/generators/strategy_registry.py

from typing import Dict, Tuple, Callable
from euromillions.generators.strategies.modulo_increment import generate_modulo_increment
from euromillions.generators.strategies.strategy_example import generate_strategy_example

StrategyVariant = Tuple[Callable, dict]

def get_all_strategy_variants() -> Dict[str, StrategyVariant]:
    """
    Named strategy variants mapped to their generating function and parameters.
    """
    return {
        "example": (generate_strategy_example, {}),

        "modulo_1": (generate_modulo_increment, {"start": 1, "increment": 2}),
        "modulo_2": (generate_modulo_increment, {"start": 3, "increment": 5}),
        "modulo_3": (generate_modulo_increment, {"start": 7, "increment": 4}),
        "modulo_4": (generate_modulo_increment, {"start": 10, "increment": 1}),
        "modulo_5": (generate_modulo_increment, {"start": 2, "increment": 6}),
    }

def get_strategy_variant(index: int) -> StrategyVariant:
    """
    Indexed access for genomes: 0,1,2, etc.
    """
    variants = list(get_all_strategy_variants().values())
    return variants[index]
