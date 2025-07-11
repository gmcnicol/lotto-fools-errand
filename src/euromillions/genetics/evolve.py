import random
from typing import List, Tuple
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.genetics.fitness import evaluate_ticket_set
from euromillions.euromillions_loader import load_draws_df, load_prizes_df

Chromosome = List[int]
Population = List[Chromosome]

def generate_random_chromosome(length: int) -> Chromosome:
    return [random.randint(0, 1) for _ in range(length)]

def mutate_chromosome(chromosome: Chromosome, mutation_rate: float = 0.1) -> Chromosome:
    return [gene if random.random() > mutation_rate else 1 - gene for gene in chromosome]

def crossover(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def evaluate_chromosome(chromosome: Chromosome, draws_df, prizes_df, all_variants) -> float:
    selected = [v for g, v in zip(chromosome, all_variants) if g]
    if not selected:
        return 0.0
    tickets = generate_tickets_from_variants(draws_df, selected)
    return evaluate_ticket_set(tickets, draws_df, prizes_df)

def run_genetic_algorithm():
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()
    all_variants = get_all_strategy_variants()
    chrom_len = len(all_variants)
    population_size = 20
    generations = 10000
    stagnation_limit = 5

    population = [generate_random_chromosome(chrom_len) for _ in range(population_size)]
    best_chromosome = None
    best_score = 0.0
    no_improve_count = 0

    for gen in range(generations):
        scored = [(chromo, evaluate_chromosome(chromo, draws_df, prizes_df, all_variants)) for chromo in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:5]
        population = [c for c, _ in top]

        if top[0][1] > best_score:
            best_score = top[0][1]
            best_chromosome = top[0][0]
            no_improve_count = 0
        else:
            no_improve_count += 1

        while len(population) < population_size:
            p1, p2 = random.sample(top, 2)
            child = mutate_chromosome(crossover(p1[0], p2[0]))
            population.append(child)

        if no_improve_count >= stagnation_limit:
            break

    print("Best Chromosome:", best_chromosome)
    print("Best Score:", best_score)

    selected = [v for g, v in zip(best_chromosome, all_variants) if g]
    tickets = generate_tickets_from_variants(draws_df, selected)
    print("Suggested Tickets:")
    for line in tickets[:10]:
        print("Numbers:", line[0], "Stars:", line[1])
