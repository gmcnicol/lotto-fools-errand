from euromillions.genetics.genome import generate_random_chromosome, evaluate_chromosome
from euromillions.generators.strategy_registry import get_all_strategy_variants

def run_all_genomes():
    strategy_count = len(get_all_strategy_variants())
    for _ in range(5):
        chromo = generate_random_chromosome(strategy_count)
        score = evaluate_chromosome(chromo)
        print("Chromosome:", chromo, "Score:", score)
