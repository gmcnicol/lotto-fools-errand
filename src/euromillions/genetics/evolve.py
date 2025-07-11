import random
from typing import List
from euromillions.genetics.genome import Chromosome, generate_random_chromosome, mutate_chromosome, evaluate_chromosome
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.euromillions_loader import load_draws_df

def run_evolution(
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1,
        convergence_limit: int = 5,
):
    draws_df = load_draws_df()
    strategy_variants = get_all_strategy_variants()
    chromosome_length = len(strategy_variants)

    population: List[Chromosome] = [
        generate_random_chromosome(chromosome_length)
        for _ in range(population_size)
    ]

    best_score = 0.0
    best_chromosome = None
    no_improvement_generations = 0

    for generation in range(generations):
        scored_population = [
            (chromosome, evaluate_chromosome(chromosome))
            for chromosome in population
        ]

        scored_population.sort(key=lambda x: x[1], reverse=True)
        best_in_generation = scored_population[0]

        print(f"Generation {generation + 1}: Best Score = {best_in_generation[1]}, Chromosome = {best_in_generation[0]}")

        if best_in_generation[1] > best_score:
            best_score = best_in_generation[1]
            best_chromosome = best_in_generation[0]
            no_improvement_generations = 0
        else:
            no_improvement_generations += 1

        if no_improvement_generations >= convergence_limit:
            print(f"Converged after {generation + 1} generations.")
            break

        # Selection (top 25%)
        survivors = [chrom for chrom, _ in scored_population[: population_size // 4]]

        # Crossover
        children = []
        while len(children) + len(survivors) < population_size:
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            split = random.randint(1, chromosome_length - 1)
            child = parent1[:split] + parent2[split:]
            children.append(child)

        # Mutation
        mutated = [mutate_chromosome(chrom, mutation_rate) for chrom in children]

        # New population
        population = survivors + mutated

    print("\n🏆 Best Chromosome Found:", best_chromosome)
    print("Fitness Score:", best_score)

    # Show the tickets from this chromosome
    selected_variants = [
        variant for gene, variant in zip(best_chromosome, strategy_variants) if gene
    ]
    if not selected_variants:
        print("No active strategies in final chromosome.")
        return

    tickets = generate_tickets_from_variants(draws_df, selected_variants)
    print("\n🎟️ Suggested Tickets to Play:")
    for i, (numbers, stars) in enumerate(tickets[:10], 1):
        print(f"{i:2d}: Numbers={numbers}, Stars={stars}")
