from typing import List, Tuple, Callable
from euromillions.generators.strategies.modulo_increment import generate_modulo_increment
from euromillions.generators.strategies.strategy_example import generate_strategy_example

# Each strategy is represented as a (function, parameter_dict) tuple
strategy_variants: List[Tuple[Callable, dict]] = [
    (generate_strategy_example, {}),
    (generate_modulo_increment, {"start": 1, "increment": 2}),
    (generate_modulo_increment, {"start": 3, "increment": 5}),
    (generate_modulo_increment, {"start": 7, "increment": 4}),
    (generate_modulo_increment, {"start": 10, "increment": 1}),
    (generate_modulo_increment, {"start": 2, "increment": 6}),
]

def get_all_strategy_variants() -> List[Tuple[Callable, dict]]:
    return strategy_variants