from typing import Dict, Callable

from . import strategy_example  # Add new ones here

def get_all_strategies() -> Dict[str, Callable]:
    """
    Return all available ticket generation strategies.
    Each must conform to:
    def strategy(draws_df: pd.DataFrame, step: int, window: int) -> List[Ticket]
    """
    return {
        "strategy_example": strategy_example.generate
    }
