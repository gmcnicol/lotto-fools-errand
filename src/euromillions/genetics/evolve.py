# src/euromillions/genetics/evolve.py

import os
import logging
import random

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# Configure logger
logger = logging.getLogger(__name__)
if os.environ.get("LOGLEVEL", "").lower() == "debug":
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)

# GA parameters
POPULATION_SIZE = 50
GENERATIONS = 10000
MUTATION_RATE = 0.1
ELITE_SIZE = 10
MAX_TICKETS = 7


def initialize_population(num_strategies: int, population_size: int) -> list[list[int]]:
    """
    Create an initial population of random binary chromosomes.
    """
    return [
        [random.choice([0, 1]) for _ in range(num_strategies)]
        for __ in range(population_size)
    ]


def mutate(chromosome: list[int]) -> list[int]:
    """
    Flip each gene with probability MUTATION_RATE.
    """
    mutated = chromosome[:]
    mutated_flag = False
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = 1 - mutated[i]
            logger.debug(f"Mutation: gene {i} flipped {chromosome} → {mutated}")
            mutated_flag = True
    if not mutated_flag:
        logger.debug(f"No mutation for {chromosome}")
    return mutated


def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    """
    Single‐point crossover between two parents.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be same length")
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    logger.debug(f"Crossover: {parent1} x {parent2} @ {point} → {child}")
    return child


def run_evolution():
    # Load historical draws and prizes
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    # Build the exhaustive list of strategy‐parameter variants
    variants = get_all_strategy_variants()
    num_strategies = len(variants)

    # Initialize population
    population = initialize_population(num_strategies, POPULATION_SIZE)
    fitness_scores: list[tuple[float, list[int]]] = []
    seen: set[tuple[int, ...]] = set()

    for gen in range(1, GENERATIONS + 1):
        logger.info(f"\n=== Generation {gen} ===")

        # Evaluate each chromosome
        for chrom in population:
            tickets = generate_tickets_from_variants(
                chromosome=chrom,
                variants=variants,
                draws_df=draws_df,
                max_tickets=MAX_TICKETS,
            )
            fitness = evaluate_ticket_set(tickets, draws_df, prizes_df)
            fitness_scores.append((fitness, chrom))
            logger.info(f"Fitness: {fitness:.2f}")


        # Sort descending by fitness
        fitness_scores.sort(key=lambda x: x[0], reverse=True)
        # Keep the elites
        elites = [chrom for (_, chrom) in fitness_scores[:ELITE_SIZE]]
        logger.info(f"Top fitness scores: {fitness_scores[:ELITE_SIZE]}")

        # Build next generation
        next_pop = elites[:]  # carry over
        seen.update(tuple(c) for c in population)

        logger.info(f"seen chromosomes: {len(seen)}")
        # Fill up to POPULATION_SIZE with offspring
        while len(next_pop) < POPULATION_SIZE:
            p1, p2 = random.sample(elites, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            t = tuple(child)
            if t not in seen:
                next_pop.append(child)

        population = next_pop

    # After last generation, take the very best
    best_fitness, best_chrom = max(
        fitness_scores, key=lambda x: x[0]
    )
    logger.info(f"\n*** Evolution complete ***")
    logger.info(f"Best fitness: {best_fitness:.2f}")
    logger.info(f"Best chromosome: {best_chrom}")

    # Generate and print the final ticket suggestions
    best_tickets = generate_tickets_from_variants(
        chromosome=best_chrom,
        variants=variants,
        draws_df=draws_df,
        max_tickets=MAX_TICKETS,
    )
    logger.info("Suggested Tickets:")
    for nums, stars in best_tickets:
        logger.info(f"Numbers: {nums}  Stars: {stars}")
