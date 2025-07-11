from euromillions.generators.strategies.modulo_increment import generate_modulo_increment

strategy_variants = [
    (generate_modulo_increment, {"start": 1, "increment": 2}),
    (generate_modulo_increment, {"start": 3, "increment": 5}),
    (generate_modulo_increment, {"start": 7, "increment": 4}),
    (generate_modulo_increment, {"start": 10, "increment": 1}),
]

def get_all_strategy_variants():
    return strategy_variants
