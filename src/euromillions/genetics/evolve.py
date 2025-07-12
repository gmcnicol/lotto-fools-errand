import logging
import random
import sys
from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
ELITE_SIZE = 10
MAX_TICKETS = 7


def initialize_population(num_strategies: int, population_size: int) -> list[list[int]]:
    logger.info(f"Initializing population with {population_size} chromosomes, each with {num_strategies} genes.")
    population = []
    for _ in range(population_size):
        chromosome = [random.choice([0, 1]) for _ in range(num_strategies)]
        population.append(chromosome)
    logger.info("Population initialization complete.")
    return population


def mutate(chromosome: list[int]) -> list[int]:
    mutated = chromosome[:]
    mutation_occurred = False
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = 1 - mutated[i]
            logger.debug(f"Mutation: gene {i} flipped in {chromosome} → {mutated}")
            mutation_occurred = True
    if mutation_occurred:
        logger.info(f"Chromosome mutated: {chromosome} → {mutated}")
    else:
        logger.debug(f"No mutation in {chromosome}")
    return mutated


def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be the same length")
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    logger.info(f"Crossover at point {point}: {parent1} x {parent2} → {child}")
    return child


def run_evolution():
    logger.info("Starting evolutionary algorithm.")
    draws_df = load_draws_df()
    prizes_df = load_prizes_df()

    variants = get_all_strategy_variants()
    num_strategies = len(variants)

    population = initialize_population(num_strategies, POPULATION_SIZE)

    for generation in range(GENERATIONS):
        logger.info(f"\nGeneration {generation + 1}")
        fitness_scores = []

        for chromosome in population:
            tickets = generate_tickets_from_variants(chromosome, variants, draws_df, MAX_TICKETS)
            fitness = evaluate_ticket_set(tickets, draws_df, prizes_df)
            fitness_scores.append((fitness, chromosome))
            logger.info(f"Fitness: {fitness:.2f} for chromosome {chromosome}")

        fitness_scores.sort(reverse=True, key=lambda x: x[0])
        elites = [chrom for _, chrom in fitness_scores[:ELITE_SIZE]]
        logger.info(f"Selected {ELITE_SIZE} elites for next generation.")

        next_generation = elites[:]
        seen = set(tuple(chrom) for chrom in elites)

        while len(next_generation) < POPULATION_SIZE:
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            if parent1 == parent2:
                continue
            child = crossover(parent1, parent2)
            child = mutate(child)
            t_child = tuple(child)
            if t_child not in seen:
                next_generation.append(child)
                seen.add(t_child)
                logger.info(f"Added new child to next generation: {child}")

        logger.info(f"Generation {generation + 1} complete. Population size: {len(next_generation)}")
        population = next_generation

    logger.info("Evolutionary algorithm finished.")