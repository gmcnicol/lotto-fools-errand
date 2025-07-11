# src/euromillions/genetics/genome.py

import random
from typing import List, Tuple
from euromillions.genetics.strategy_registry import get_strategy_variants
from euromillions.genetics.fitness import evaluate_chromosome_fitness
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Chromosome = List[int]


def generate_initial_population(pop_size: int, chromosome_length: int) -> List[Chromosome]:
    return [
        [random.randint(0, 1) for _ in range(chromosome_length)]
        for _ in range(pop_size)
    ]


def mutate_chromosome(chromosome: Chromosome, mutation_rate: float) -> Chromosome:
    return [
        gene if random.random() > mutation_rate else 1 - gene
        for gene in chromosome
    ]


def crossover_chromosomes(parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
    point = random.randint(1, len(parent1) - 1)
    return (
        parent1[:point] + parent2[point:],
        parent2[:point] + parent1[point:]
    )


def run_evolutionary_algorithm(
        generations: int = 10,
        pop_size: int = 20,
        mutation_rate: float = 0.1
):
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()
    strategy_variants = get_strategy_variants()
    chromosome_length = len(strategy_variants)

    population = generate_initial_population(pop_size, chromosome_length)

    for generation in range(generations):
        scored = []
        for chromosome in population:
            score = evaluate_chromosome_fitness(
                draws_df=draws_df,
                prizes_df=prizes_df,
                chromosome=chromosome
            )
            scored.append((score, chromosome))

        scored.sort(reverse=True, key=lambda x: x[0])
        best_score, best_chromosome = scored[0]
        print(f"Generation {generation} | Best score: £{best_score:.2f} | Genome: {best_chromosome}")

        new_population = [best_chromosome]

        while len(new_population) < pop_size:
            parent1 = random.choice(scored[:10])[1]
            parent2 = random.choice(scored[:10])[1]
            child1, child2 = crossover_chromosomes(parent1, parent2)
            new_population.extend([
                mutate_chromosome(child1, mutation_rate),
                mutate_chromosome(child2, mutation_rate)
            ])

        population = new_population[:pop_size]
