import random
from typing import Optional

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# ─────────────────────────────────────────────────────────────
# GA PARAMETERS (tweak at will)
POPULATION_SIZE    = 65
ELITE_SIZE         = 15
MAX_TICKETS        = 7

MUTATION_RATE      = 0.09
MAX_GENERATIONS    = 10_000
CONVERGENCE_WINDOW = 200

# SLIDING WINDOW: how many of the most‐recent draws to train on each step.
#   None → use all draws from the start up to the current one.
SLIDING_WINDOW: Optional[int] = 11
# ─────────────────────────────────────────────────────────────


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
    draws_df  = load_draws_df()
    prizes_df = load_prizes_df()
    variants  = get_all_strategy_variants()
    num_strategies = len(variants)

    # initial random pop
    population = initialize_population(num_strategies, POPULATION_SIZE)

    # step through each historical draw in turn
    for draw_idx, draw_row in draws_df.iterrows():
        # build the window of draws to train on
        if SLIDING_WINDOW is None:
            window_start = 0
        else:
            window_start = max(0, draw_idx - SLIDING_WINDOW + 1)

        window_df = draws_df.iloc[window_start : draw_idx + 1]
        print(f"\n=== Draw {draw_idx + 1}/{len(draws_df)} "
              f"({draw_row['date']}) → using window of {len(window_df)} draws ===")

        best_fitness    = float("-inf")
        best_chromosome = None
        no_improve      = 0

        for gen in range(1, MAX_GENERATIONS + 1):
            # evaluate entire population on this window
            scored: list[tuple[float, list[int]]] = []
            for chrom in population:
                tickets = generate_tickets_from_variants(
                    chrom, variants, window_df, MAX_TICKETS
                )
                fitness = evaluate_ticket_set(tickets, window_df, prizes_df)
                scored.append((fitness, chrom))

            # pick the current-gen best
            scored.sort(key=lambda x: x[0], reverse=True)
            current_best, current_chrom = scored[0]

            # improvement?
            if current_best > best_fitness:
                best_fitness    = current_best
                best_chromosome = current_chrom
                no_improve      = 0
            else:
                no_improve += 1

            # status every 1,000 gens
            if gen % 1000 == 0:
                print(f" Gen {gen:5d}: best fitness so far = {best_fitness:.2f}")

            # convergence check
            if no_improve >= CONVERGENCE_WINDOW:
                print(
                    f" Converged after {gen} gens "
                    f"(no improve in last {CONVERGENCE_WINDOW}), "
                    f"best fitness = {best_fitness:.2f}"
                )
                break

            # build next generation: keep ELITE_SIZE, then fill by crossover+mutation
            elites = [chrom for _, chrom in scored[:ELITE_SIZE]]
            next_pop = elites.copy()
            while len(next_pop) < POPULATION_SIZE:
                p1, p2 = random.sample(elites, 2)
                child  = mutate(crossover(p1, p2))
                next_pop.append(child)

            population = next_pop

        # carry forward only the elites into the next draw’s GA
        elites = [chrom for _, chrom in scored[:ELITE_SIZE]]
        population = elites.copy()
        while len(population) < POPULATION_SIZE:
            population.append(mutate(random.choice(elites)))

    # end of all draws → best_chromosome is from the last draw’s GA
    print("\n=== Final Best Chromosome ===")
    final_tickets = generate_tickets_from_variants(
        best_chromosome, variants, draws_df, MAX_TICKETS
    )
    for idx, (nums, stars) in enumerate(final_tickets, start=1):
        print(f"Ticket {idx}: numbers={nums}, stars={stars}")
