import random
from typing import List, Tuple
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.genetics.fitness import evaluate_ticket_set
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Chromosome = List[int]

def generate_random_chromosome(length: int) -> Chromosome:
    return [random.randint(0, 1) for _ in range(length)]

def mutate_chromosome(chromosome: Chromosome, mutation_rate: float = 0.1) -> Chromosome:
    return [
        gene if random.random() > mutation_rate else 1 - gene
        for gene in chromosome
    ]

def evaluate_chromosome(chromosome: Chromosome) -> float:
    all_variants = get_all_strategy_variants()
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    selected_variants = [
        variant for gene, variant in zip(chromosome, all_variants) if gene
    ]

    if not selected_variants:
        return 0.0

    tickets = generate_tickets_from_variants(draws_df, selected_variants)
    return evaluate_ticket_set(tickets, draws_df, prizes_df)

def run_evolution(
        population_size: int = 100,
        generations: int = 10000,
        patience: int = 5,
        mutation_rate: float = 0.1,
        top_k: int = 5
):
    all_variants = get_all_strategy_variants()
    chromosome_length = len(all_variants)

    population = [
        generate_random_chromosome(chromosome_length)
        for _ in range(population_size)
    ]

    best_chromosomes = []
    best_score = float('-inf')
    stagnation = 0

    for generation in range(generations):
        scored = [(chromo, evaluate_chromosome(chromo)) for chromo in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:top_k]

        print(f"Generation {generation}, Best score: {top[0][1]}")
        if top[0][1] > best_score:
            best_score = top[0][1]
            best_chromosomes = [top[0]]
            stagnation = 0
        elif top[0][1] == best_score:
            best_chromosomes.append(top[0])
            stagnation += 1
        else:
            stagnation += 1

        if stagnation >= patience:
            break

        new_population = [chromo for chromo, _ in top]
        while len(new_population) < population_size:
            parent = random.choice(top)[0]
            child = mutate_chromosome(parent, mutation_rate)
            new_population.append(child)

        population = new_population

    fittest = best_chromosomes[-1]
    print(f"\nFittest Chromosome: {fittest} with score: {best_score}\n")

    draws_df = load_draws_df()
    selected_variants = [
        variant for gene, variant in zip(fittest, all_variants) if gene
    ]
    tickets = generate_tickets_from_variants(draws_df, selected_variants)

    print("Recommended Tickets:")
    for i, ticket in enumerate(tickets[:7], 1):  # limit to 7 tickets
        numbers, stars = ticket
        print(f"Ticket {i}: Numbers: {numbers}, Stars: {stars}")
