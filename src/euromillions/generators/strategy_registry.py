from euromillions.generators.strategies.modulo_increment import generate_modulo_increment

def get_all_strategy_variants():
    variants = []

    # Exhaustive scan for modulo_increment parameters
    for start in range(1, 51):  # assuming 1–50 is safe
        for increment in range(1, 11):  # increment 1–10
            variants.append((generate_modulo_increment, {'start': start, 'increment': increment}))

    return variants