import random
from typing import List

from euromillions.euromillions_loader import load_draws_df
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.genetics.fitness import evaluate_ticket_set

# Chromosome is a binary list representing active strategy variants
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

    # Filter variants based on chromosome
    selected_variants = [
        variant for gene, variant in zip(chromosome, all_variants) if gene
    ]

    if not selected_variants:
        return 0.0

    tickets = generate_tickets_from_variants(draws_df, selected_variants)
    return evaluate_ticket_set(tickets)