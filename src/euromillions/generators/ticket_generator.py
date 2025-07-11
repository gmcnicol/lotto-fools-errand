# src/euromillions/generators/ticket_generator.py

from typing import List
import pandas as pd
from euromillions.generators.strategy_registry import get_strategy_function

def generate_tickets(strategy: str, draws_df: pd.DataFrame, **kwargs) -> List[tuple]:
    """
    Generate 10 EuroMillions tickets using the selected strategy.
    """
    strategy_func = get_strategy_function(strategy)
    return strategy_func(draws_df, **kwargs)
