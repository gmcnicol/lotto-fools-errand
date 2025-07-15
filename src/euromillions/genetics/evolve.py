
import random

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# GA parameters
POPULATION_SIZE = 50
ELITE_SIZE = 10
MAX_TICKETS = 7

MUTATION_RATE = 0.1
MAX_GENERATIONS = 10_000
CONVERGENCE_WINDOW = 500


def initialize_population(num_strategies: int, population_size: int) -> list[list[int]]:
    return [
        [random.choice([0, 1]) for _ in range(num_strategies)]
        for _ in range(population_size)
    ]


def mutate(chromosome: list[int]) -> list[int]:
    mutated = chromosome[:]
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = 1 - mutated[i]
    return mutated


def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]


def run_evolution():
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()
    variants = get_all_strategy_variants()
    num_strategies = len(variants)

    # Start with a random population
    population = initialize_population(num_strategies, POPULATION_SIZE)

    # Step sequentially through each historical draw
    for draw_idx, draw_row in draws_df.iterrows():
        current_draw_df = draws_df.iloc[[draw_idx]]
        print(f"\n=== Draw {draw_idx + 1}/{len(draws_df)} ({draw_row['date']}) ===")

        best_fitness = float("-inf")
        no_improve = 0
        best_chromosome = None

        for gen in range(1, MAX_GENERATIONS + 1):
            # Evaluate all chromosomes on this single draw
            scored = []
            for chrom in population:
                tickets = generate_tickets_from_variants(
                    chrom, variants, current_draw_df, MAX_TICKETS
                )
                fitness = evaluate_ticket_set(tickets, current_draw_df, prizes_df)
                scored.append((fitness, chrom))

            # Sort descending by fitness
            scored.sort(key=lambda x: x[0], reverse=True)
            current_best, current_chrom = scored[0]

            # Check for improvement
            if current_best > best_fitness:
                best_fitness = current_best
                best_chromosome = current_chrom
                no_improve = 0
            else:
                no_improve += 1

            # Periodic status
            if gen % 1000 == 0:
                print(f" Gen {gen:5d}: best fitness so far = {best_fitness:.2f}")

            # Convergence check
            if no_improve >= CONVERGENCE_WINDOW:
                print(
                    f" Converged after {gen} generations "
                    f"(no improvement in last {CONVERGENCE_WINDOW}), "
                    f"best fitness = {best_fitness:.2f}"
                )
                break

            # Build next generation: keep elites + crossover+mutate
            elites = [chrom for _, chrom in scored[:ELITE_SIZE]]
            next_pop = elites.copy()
            while len(next_pop) < POPULATION_SIZE:
                p1, p2 = random.sample(elites, 2)
                child = mutate(crossover(p1, p2))
                next_pop.append(child)
            population = next_pop

        # Prepare for next draw: carry forward only the elites
        elites = [chrom for _, chrom in scored[:ELITE_SIZE]]
        population = elites.copy()
        while len(population) < POPULATION_SIZE:
            population.append(mutate(random.choice(elites)))

    # After all draws, best_chromosome is from the final draw
    print("\n=== Final Best Chromosome ===")
    tickets = generate_tickets_from_variants(
        best_chromosome, variants, draws_df, MAX_TICKETS
    )
    for idx, (nums, stars) in enumerate(tickets, start=1):
        print(f"Ticket {idx}: numbers={nums}, stars={stars}")
