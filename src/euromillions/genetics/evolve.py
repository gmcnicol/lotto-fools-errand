import random
from typing import List, Tuple
from euromillions.generators.strategy_registry import get_dynamic_strategy_variants
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.genetics.fitness import evaluate_ticket_set
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Chromosome = List[int]

MAX_ITERATIONS = 10_000
CONVERGENCE_COUNT = 5
TICKET_COUNT = 7
MIN_ACTIVE_STRATEGIES = 1
MAX_ACTIVE_STRATEGIES = 5


def generate_random_chromosome(length: int) -> Chromosome:
    while True:
        chromo = [random.randint(0, 1) for _ in range(length)]
        active_count = sum(chromo)
        if MIN_ACTIVE_STRATEGIES <= active_count <= MAX_ACTIVE_STRATEGIES:
            return chromo


def mutate_chromosome(chromosome: Chromosome, mutation_rate: float = 0.1) -> Chromosome:
    return [
        gene if random.random() > mutation_rate else 1 - gene
        for gene in chromosome
    ]

def crossover(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def evaluate_chromosome(chromosome: Chromosome, draws_df, prizes_df) -> Tuple[Chromosome, float]:
    all_variants = get_dynamic_strategy_variants()
    selected_variants = [
        variant for gene, variant in zip(chromosome, all_variants) if gene
    ]

    if not selected_variants:
        return chromosome, float("-inf")

    tickets = generate_tickets_from_variants(draws_df, selected_variants, limit=TICKET_COUNT)
    score = evaluate_ticket_set(tickets, draws_df, prizes_df)
    return chromosome, score

def run_evolution():
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()
    variant_count = len(get_dynamic_strategy_variants())

    population_size = 20
    population = [generate_random_chromosome(variant_count) for _ in range(population_size)]

    best_history: List[Tuple[Chromosome, float]] = []

    for gen in range(MAX_ITERATIONS):
        evaluated = [evaluate_chromosome(chromo, draws_df, prizes_df) for chromo in population]
        evaluated = [x for x in evaluated if x[1] > 0.0]  # Only keep positive-scoring chromosomes

        if not evaluated:
            print("All chromosomes had non-positive fitness.")
            break

        evaluated.sort(key=lambda x: x[1], reverse=True)
        best = evaluated[0]
        best_history.append(best)

        print(f"Gen {gen}: Best score = {best[1]} Chromosome = {best[0]}")

        # Convergence check
        if len(best_history) >= CONVERGENCE_COUNT:
            recent = best_history[-CONVERGENCE_COUNT:]
            if all(b[0] == recent[0][0] for b in recent):
                print(f"Converged after {gen + 1} generations.")
                break

        # Reproduction
        next_gen = [best[0]]  # Keep best
        while len(next_gen) < population_size:
            parent1 = random.choice(evaluated)[0]
            parent2 = random.choice(evaluated)[0]
            child = crossover(parent1, parent2)
            child = mutate_chromosome(child)
            next_gen.append(child)

        population = next_gen

    # Final best
    if best_history:
        final_best = best_history[-1]
        print("\nFinal best chromosome and tickets:")
        print("Chromosome:", final_best[0])
        final_variants = [
            v for g, v in zip(final_best[0], get_dynamic_strategy_variants()) if g
        ]
        final_tickets = generate_tickets_from_variants(draws_df, final_variants, limit=TICKET_COUNT)
        for idx, (numbers, stars) in enumerate(final_tickets, 1):
            print(f"Ticket {idx}: Numbers {sorted(numbers)}, Stars {sorted(stars)}")
