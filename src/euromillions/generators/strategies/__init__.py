# src/euromillions/generators/strategies/__init__.py

from typing import Dict, Callable
from . import strategy_example
from . import modulo_increment

from .strategy_example import generate_strategy_example
from .modulo_increment import generate_modulo_increment

def get_all_strategies() -> Dict[str, Callable]:
    """
    Return all available ticket generation strategies.
    Each must conform to:
    def strategy(draws_df: pd.DataFrame, step: int, window: int) -> List[Ticket]
    """
    return {
        "strategy_example": generate_strategy_example,
        "modulo_increment": generate_modulo_increment,
    }
