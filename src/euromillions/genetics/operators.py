import logging
import random

logger = logging.getLogger(__name__)


def crossover(parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate_chromosome(chromosome: list[int], mutation_rate: float = 0.01) -> list[int]:
    mutated = chromosome[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            old = mutated[i]
            mutated[i] = 1 - old
            logger.info(f"Mutated gene at index {i}: {old} → {mutated[i]}")
    return mutated


def select_parents(population: list[list[int]]) -> tuple[list[int], list[int]]:
    return random.choice(population), random.choice(population)
