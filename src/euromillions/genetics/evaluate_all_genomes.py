import random
from euromillions.genetics.genome import (
    generate_random_chromosome,
    mutate_chromosome,
    evaluate_chromosome,
)
from euromillions.generators.strategy_registry import get_all_strategy_variants

def run_genetic_test(population_size=10, generations=5):
    strategy_count = len(get_all_strategy_variants())
    population = [generate_random_chromosome(strategy_count) for _ in range(population_size)]

    for gen in range(generations):
        print(f"Generation {gen+1}")
        scores = [(chromosome, evaluate_chromosome(chromosome)) for chromosome in population]
        scores.sort(key=lambda x: x[1], reverse=True)

        best = scores[0]
        print(f"  Best score: {best[1]:.2f}  Genome: {best[0]}")

        # Reproduce and mutate
        top_half = [chrom for chrom, _ in scores[: population_size // 2]]
        population = top_half + [mutate_chromosome(random.choice(top_half)) for _ in range(population_size // 2)]

if __name__ == "__main__":
    run_genetic_test()