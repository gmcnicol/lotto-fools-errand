# src/euromillions/generators/strategy_registry.py

from typing import Callable
from euromillions.generators.strategies import (
    strategy_example,
    modulo_increment,
)

# Registry maps strategy name strings to the corresponding generator function
STRATEGY_REGISTRY: dict[str, Callable] = {
    "strategy_example": strategy_example.generate_strategy_example,
    "modulo_increment": modulo_increment.generate_modulo_increment,
}


def get_strategy_function(name: str) -> Callable:
    """
    Retrieve the strategy function from the registry by name.

    Args:
        name (str): Name of the strategy (e.g., 'modulo_increment')

    Returns:
        Callable: Function that implements the strategy

    Raises:
        ValueError: If the strategy is not found
    """
    try:
        return STRATEGY_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown strategy: {name}")
