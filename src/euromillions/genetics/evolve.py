# src/euromillions/genetics/evolve.py

import random

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# GA hyper-parameters
POPULATION_SIZE = 50
GENERATIONS     = 20
MUTATION_RATE   = 0.05
ELITE_SIZE      = 5
MAX_TICKETS     = 7

def initialize_population(num_strategies: int, size: int) -> list[list[int]]:
    pop = []
    for _ in range(size):
        chrom = [random.choice((0, 1)) for _ in range(num_strategies)]
        print(f"[INIT] chromosome: {chrom}")
        pop.append(chrom)
    return pop

def mutate(chromosome: list[int]) -> list[int]:
    out = chromosome[:]
    for i in range(len(out)):
        if random.random() < MUTATION_RATE:
            old = out[i]
            out[i] = 1 - old
    return out

def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

def run_evolution() -> None:
    # 1) load
    draws_df  = load_draws_df()
    prizes_df = load_prizes_df()
    if draws_df.empty:
        print("ERROR: no draws data. Run `fetch-draws` first.")
        return

    # 2) strategies
    variants       = get_all_strategy_variants()
    num_strategies = len(variants)
    print(f"[INFO] {num_strategies} total strategy variants")

    # 3) initial pop
    population = initialize_population(num_strategies, POPULATION_SIZE)
    best_so_far = None
    # 4) rolling‐horizon GA over each draw
    for step in range(1, len(draws_df)):
        history_draws  = draws_df.iloc[:step]
        history_prizes = prizes_df.iloc[:step]
        print(f"=== Evolving for draw #{step} (history size={len(history_draws)}) ===")

        for gen in range(1, GENERATIONS + 1):
            fitness_list: list[tuple[float, list[int]]] = []

            for chrom in population:
                tickets = generate_tickets_from_variants(
                    chrom, variants, history_draws, MAX_TICKETS
                )
                score = evaluate_ticket_set(tickets, history_draws, history_prizes)
                fitness_list.append((score, chrom))

            # sort + report best
            fitness_list.sort(key=lambda x: x[0], reverse=True)

            # elitism
            elites = [c for _, c in fitness_list[:ELITE_SIZE]]
            next_pop = elites.copy()
            seen = set(tuple(c) for c in elites)

            # fill rest
            while len(next_pop) < POPULATION_SIZE:
                p1, p2 = random.sample(elites, 2)
                child  = crossover(p1, p2)
                child  = mutate(child)
                tup    = tuple(child)
                if tup not in seen:
                    seen.add(tup)
                    next_pop.append(child)

            population = next_pop

        # end‐of‐step champion
        final_score, final_chrom = fitness_list[0]
        # print(f"→ Champion for draw #{step}: (score {final_score:.2f}) {final_chrom} ")

        # seed next step
        # Use the best chromosome found so far as the seed for the next population
        population = [final_chrom] + [
            mutate(final_chrom) for _ in range(POPULATION_SIZE - 1)
        ]
        # Compare best_so_far with the best mutation of the current run
        mutated_chroms = [mutate(final_chrom) for _ in range(POPULATION_SIZE - 1)]
        print(f"[PROGRESS] Generated {len(mutated_chroms)} mutated chromosomes for evaluation.")
        mutated_scores = [
            evaluate_ticket_set(
                generate_tickets_from_variants(chrom, variants, draws_df, MAX_TICKETS),
                draws_df, prizes_df
            )
            for chrom in mutated_chroms
        ]
        print(f"[PROGRESS] Evaluated mutated chromosomes. Scores: {mutated_scores}")
        best_mutation_score = max(mutated_scores) if mutated_scores else float('-inf')
        print(f"[PROGRESS] Best mutation score: {best_mutation_score}")
        if best_so_far is None:
            print("[PROGRESS] No best_so_far yet. Setting to final_chrom.")
            best_so_far = final_chrom
        else:
            # Evaluate fitness of best_so_far
            best_so_far_score = evaluate_ticket_set(
                generate_tickets_from_variants(best_so_far, variants, draws_df, MAX_TICKETS),
                draws_df, prizes_df
            )
            print(f"[PROGRESS] Current best_so_far score: {best_so_far_score}")
            if final_score >= best_mutation_score:
                print(f"[PROGRESS] final_score ({final_score}) >= best_mutation_score ({best_mutation_score}). Updating best_so_far to final_chrom.")
                best_so_far = final_chrom
                best_mutation_score = final_score
            else:
                # Find the best mutation
                idx = mutated_scores.index(best_mutation_score)
                best_mutation = mutated_chroms[idx]
                print(f"[PROGRESS] Best mutation found at index {idx} with score {best_mutation_score}. Updating best_so_far.")
                best_so_far = best_mutation
                best_score_so_far = best_mutation_score

    # 5) final suggestion
    if best_so_far is None:
        print("ERROR: no best chromosome found.")
        return

    print("\n=== Suggested Tickets for Next Draw ===")
    suggested = generate_tickets_from_variants(best_so_far, variants, draws_df, MAX_TICKETS)
    for nums, stars in suggested:
        print("Numbers:", nums, "Stars:", stars)
