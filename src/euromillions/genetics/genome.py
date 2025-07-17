import random
from typing import List
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.genetics.fitness import evaluate_ticket_set
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Chromosome = List[int]
MAX_ACTIVE_STRATEGIES = 4  # Example limit

def generate_random_chromosome(length: int, max_active: int = MAX_ACTIVE_STRATEGIES) -> Chromosome:
    chromosome = [0] * length
    active_indices = random.sample(range(length), k=min(max_active, length))
    for idx in active_indices:
        chromosome[idx] = 1
    return chromosome

def mutate_chromosome(chromosome: Chromosome, mutation_rate: float = 0.1, max_active: int = MAX_ACTIVE_STRATEGIES) -> Chromosome:
    mutated = [
        gene if random.random() > mutation_rate else 1 - gene
        for gene in chromosome
    ]

    # Enforce max active
    active_indices = [i for i, gene in enumerate(mutated) if gene]
    if len(active_indices) > max_active:
        to_deactivate = random.sample(active_indices, len(active_indices) - max_active)
        for idx in to_deactivate:
            mutated[idx] = 0

    return mutated

def evaluate_chromosome(chromosome: Chromosome) -> float:
    all_variants = get_all_strategy_variants()
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    selected_variants = [
        variant for gene, variant in zip(chromosome, all_variants) if gene
    ]
    if not selected_variants:
        return 0.0

    tickets = generate_tickets_from_variants(
        chromosome,
        selected_variants,
        draws_df,
        max_tickets=7,
    )
    return evaluate_ticket_set(tickets, draws_df, prizes_df)
