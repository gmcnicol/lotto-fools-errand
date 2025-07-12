import random

def mutate_chromosome(chromosome, mutation_rate):
    mutated = chromosome.copy()
    for idx in range(len(mutated)):
        if random.random() < mutation_rate:
            original = mutated[idx]
            mutated[idx] = 1 - mutated[idx]
            print(f"Mutating gene at index {idx} from {original} to {mutated[idx]}")
    return mutated
