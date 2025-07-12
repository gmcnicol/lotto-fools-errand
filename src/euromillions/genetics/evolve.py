import random
from typing import List, Tuple

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.genetics.fitness import evaluate_ticket_set
from euromillions.generators.ticket_generator import generate_tickets_from_variants

Genome = List[int]
Population = List[Genome]

def select_parents(population: Population, scores: List[float]) -> Tuple[Genome, Genome]:
    return random.choices(population, weights=scores, k=2)

def crossover(parent1: Genome, parent2: Genome) -> Genome:
    point = random.randint(1, len(parent1) - 2)
    child = parent1[:point] + parent2[point:]
    print(f"Crossover at {point}: {parent1} + {parent2} => {child}")
    return child

def mutate(genome: Genome, rate: float) -> Genome:
    mutated = genome[:]
    mutated_flag = False
    for i in range(len(mutated)):
        if random.random() < rate:
            mutated[i] = 1 - mutated[i]
            mutated_flag = True
            print(f"Mutation at gene {i}: flipped to {mutated[i]}")
    if not mutated_flag:
        print("No mutation occurred on this genome.")
    return mutated

def run_evolution(
        generations: int = 200,
        population_size: int = 50,
        mutation_rate: float = 0.05,
        max_active: int = 5,
        max_tickets: int = 7,
        variant_count: int = 500,
):
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()
    variants = strategy_registry[:variant_count]
    genome_length = len(variants)

    def evaluate(chromosome: Genome) -> float:
        try:
            tickets = generate_tickets_from_variants(
                chromosome,
                variants,
                draws_df=draws_df,
                max_tickets=max_tickets
            )
            return evaluate_ticket_set(tickets, draws_df, prizes_df)
        except Exception as e:
            print(f"Error evaluating chromosome: {e}")
            return float('-inf')

    # Initialize random population
    population = [
        [1 if i < max_active else 0 for i in random.sample(range(genome_length), genome_length)]
        for _ in range(population_size)
    ]

    best_overall = (None, float('-inf'))
    for generation in range(generations):
        print(f"\nGeneration {generation + 1}")

        scored = [(chromosome, evaluate(chromosome)) for chromosome in population]
        scored.sort(key=lambda x: x[1], reverse=True)

        for _, score in scored:
            print(f"Fitness: {score:.2f}")

        if scored[0][1] > best_overall[1]:
            best_overall = scored[0]

        # Elitism: carry over top N
        new_population = [c for c, _ in scored[:5]]
        existing = set(tuple(c) for c in new_population)

        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, [max(f, 0.1) for _, f in scored])
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            child_key = tuple(child)
            if child_key not in existing:
                new_population.append(child)
                existing.add(child_key)

        population = new_population

    best_chromosome, best_score = best_overall
    print("\nBest Chromosome:")
    print(best_chromosome)
    print(f"Best Fitness: {best_score:.2f}")
