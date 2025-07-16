# src/euromillions/genetics/evolve.py

import random

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# ─────────────────────────────────────────────────────────────────────────────
# GA PARAMETERS
POPULATION_SIZE    = 60       # number of chromosomes
MAX_TICKETS        = 7        # tickets per chromosome
MUTATION_RATE      = 0.11      # per-gene flip probability
MAX_GENERATIONS    = 100_000   # max iters per draw‐step
CONVERGENCE_WINDOW = 1000      # stop if no improvement in this many gens
SLIDING_WINDOW     = 20        # None ⇒ use all past; int ⇒ only last W draws
# ─────────────────────────────────────────────────────────────────────────────

def initialize_population(length: int, size: int) -> list[list[int]]:
    return [
        [random.choice([0,1]) for _ in range(length)]
        for _ in range(size)
    ]

def crossover(p1: list[int], p2: list[int]) -> list[int]:
    pt = random.randint(1, len(p1)-1)
    return p1[:pt] + p2[pt:]

def mutate(chrom: list[int]) -> list[int]:
    out = chrom[:]
    for i in range(len(out)):
        if random.random() < MUTATION_RATE:
            out[i] = 1 - out[i]
    return out

def run_evolution():
    draws_df  = load_draws_df()
    prizes_df = load_prizes_df()
    variants  = get_all_strategy_variants()
    num_strat = len(variants)

    # initial population
    population = initialize_population(num_strat, POPULATION_SIZE)
    scores     = [0.0] * POPULATION_SIZE

    best_global_score = float("-inf")
    best_global_chrom = None

    for draw_idx, draw_row in draws_df.iterrows():
        # determine window of draws to train on
        if SLIDING_WINDOW is not None and draw_idx+1 < SLIDING_WINDOW:
            continue  # not enough history yet
        window_start = 0 if SLIDING_WINDOW is None else max(0, draw_idx - SLIDING_WINDOW + 1)
        window_df    = draws_df.iloc[window_start: draw_idx+1]

        print(f"\n=== Draw {draw_idx+1}/{len(draws_df)} "
              f"({draw_row['date']}) using last "
              f"{len(window_df)} draws ===")

        # initial scoring on this window
        scores = []
        for chrom in population:
            tickets = generate_tickets_from_variants(
                chrom, variants, window_df, MAX_TICKETS
            )
            scores.append(evaluate_ticket_set(tickets, window_df, prizes_df))

        best_local_score = max(scores)
        best_local_chrom  = population[scores.index(best_local_score)]
        no_improve = 0

        # steady‐state evolution on this window
        for gen in range(1, MAX_GENERATIONS+1):
            # breed one child
            p1, p2 = random.sample(population, 2)
            child  = mutate(crossover(p1, p2))

            # score it
            tickets = generate_tickets_from_variants(
                child, variants, window_df, MAX_TICKETS
            )
            child_sc = evaluate_ticket_set(tickets, window_df, prizes_df)

            # insert + truncate worst
            population.append(child)
            scores.append(child_sc)
            paired = list(zip(scores, population))
            paired.sort(key=lambda x: x[0], reverse=True)
            paired = paired[:POPULATION_SIZE]
            scores, population = zip(*paired)
            scores     = list(scores)
            population = list(population)

            # check improvement
            if scores[0] > best_local_score:
                best_local_score = scores[0]
                best_local_chrom = population[0]
                no_improve = 0
            else:
                no_improve += 1

            if gen % 1000 == 0:
                print(f" Gen {gen:5d}: best = {best_local_score:.2f}")

            if no_improve >= CONVERGENCE_WINDOW:
                print(
                    f" Converged at gen {gen} "
                    f"(no improve in last {CONVERGENCE_WINDOW}), "
                    f"best = {best_local_score:.2f}"
                )
                break

        print(f"→ Best fitness for draw {draw_idx+1}: {best_local_score:.2f}")

        # carry forward the top POPULATION_SIZE (already done by truncation)
        # update all‐time best
        if best_local_score > best_global_score:
            best_global_score = best_local_score
            best_global_chrom = best_local_chrom

    # ─────────────────────────────────────────────────────────────────────────
    # Final output
    # ─────────────────────────────────────────────────────────────────────────
    print("\n=== Final Recommended Tickets ===")
    tickets = generate_tickets_from_variants(
        best_global_chrom, variants, draws_df, MAX_TICKETS
    )

    # normalize, sort, zero-pad
    formatted: list[tuple[list[str], list[str]]] = []
    for nums, stars in tickets:
        nums_int  = sorted(int(n) for n in nums)
        stars_int = sorted(int(s) for s in stars)
        nums_str  = [f"{n:02d}" for n in nums_int]
        stars_str = [f"{s:02d}" for s in stars_int]
        formatted.append((nums_str, stars_str))

    # print aligned table
    print(f"{'Ticket':<6} | {'Numbers':<17} | {'Stars'}")
    print(f"{'-'*6}-+-{'-'*17}-+-{'-'*5}")
    for idx, (nstrs, sstrs) in enumerate(formatted, start=1):
        print(f"{idx:<6} | {' '.join(nstrs):<17} | {' '.join(sstrs)}")

if __name__ == "__main__":
    run_evolution()
