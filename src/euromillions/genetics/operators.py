import random


def mutate(chromosome, mutation_rate=0.05):
    return [
        gene if random.random() > mutation_rate else 1 - gene
        for gene in chromosome
    ]


def crossover(parent1, parent2):
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of same length")
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2
