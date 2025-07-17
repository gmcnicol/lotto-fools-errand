# src/euromillions/genetics/evolve.py

import random
from typing import List, Tuple
import pandas as pd

from euromillions.euromillions_loader import load_draws_df, load_prizes_df
from euromillions.generators.strategy_registry import (
    get_all_strategy_variants,
    generate_tickets_from_variants,
)
from euromillions.genetics.fitness import evaluate_ticket_set

# ─────────────────────────────────────────────────────────────────────────────
# GA PARAMETERS
POPULATION_SIZE    = 100      # number of chromosomes
MAX_TICKETS        = 7       # tickets per chromosome
MUTATION_RATE      = 0.1     # per-gene flip probability
MAX_GENERATIONS    = 100_000 # max iters per draw‐step
CONVERGENCE_WINDOW = 1000    # stop if no improvement in this many gens
SLIDING_WINDOW     = 10      # None ⇒ use all past; int ⇒ only last W draws
# ─────────────────────────────────────────────────────────────────────────────

Chromosome = List[int]
Ticket     = Tuple[List[int], List[int]]
Formatted  = Tuple[List[str], List[str]]


def initialize_population(length: int, size: int) -> List[Chromosome]:
    return [
        [random.choice([0, 1]) for _ in range(length)]
        for _ in range(size)
    ]


def crossover(p1: Chromosome, p2: Chromosome) -> Chromosome:
    pt = random.randint(1, len(p1) - 1)
    return p1[:pt] + p2[pt:]


def mutate(chrom: Chromosome) -> Chromosome:
    out = chrom[:]
    for i in range(len(out)):
        if random.random() < MUTATION_RATE:
            out[i] = 1 - out[i]
    return out


def score_chromosome(
        chrom: Chromosome,
        variants: List,
        window_df: pd.DataFrame,
        prizes_df: pd.DataFrame
) -> float:
    tickets = generate_tickets_from_variants(chrom, variants, window_df, MAX_TICKETS)
    raw_score = evaluate_ticket_set(tickets, window_df, prizes_df)
    return raw_score / len(window_df)


def evolve_window(
        population: List[Chromosome],
        scores: List[float],
        variants: List,
        window_df: pd.DataFrame,
        prizes_df: pd.DataFrame
) -> Tuple[List[Chromosome], List[float], Chromosome, float]:
    best_score = max(scores)
    best_chrom = population[scores.index(best_score)]
    no_improve = 0

    for gen in range(1, MAX_GENERATIONS + 1):
        # Steady‐state: breed one child, score it, insert + drop worst
        p1, p2 = random.sample(population, 2)
        child = mutate(crossover(p1, p2))
        child_score = score_chromosome(child, variants, window_df, prizes_df)

        population.append(child)
        scores.append(child_score)

        # truncate back to POPULATION_SIZE
        paired = sorted(
            zip(scores, population),
            key=lambda x: x[0],
            reverse=True
        )[:POPULATION_SIZE]

        # unzip back into two lists
        scores_tuple, population_tuple = zip(*paired)
        scores = list(scores_tuple)
        population = list(population_tuple)

        current_best_score = scores[0]
        if current_best_score > best_score:
            best_score = current_best_score
            best_chrom = population[0]
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= CONVERGENCE_WINDOW:
            break

    return population, scores, best_chrom, best_score


def report_draw(
        draw_idx: int,
        draw_row: pd.Series,
        best_chrom: Chromosome,
        variants: List,
        window_df: pd.DataFrame
):
    # 1) Show the actual draw
    draw_nums = sorted(int(n) for n in draw_row["numbers"])
    draw_strs = sorted(int(s) for s in draw_row["stars"])
    nums_s = " ".join(f"{n:02d}" for n in draw_nums)
    strs_s = " ".join(f"{s:02d}" for s in draw_strs)
    print(f"Draw {draw_idx + 1}: {nums_s} - {strs_s}")

    # 2) Generate best tickets for this draw
    raw_tickets = generate_tickets_from_variants(best_chrom, variants, window_df, MAX_TICKETS)

    # 3) Deduplicate
    seen = set()
    unique = []
    for nums, stars in raw_tickets:
        key = (
            tuple(sorted(int(x) for x in nums)),
            tuple(sorted(int(x) for x in stars))
        )
        if key not in seen:
            seen.add(key)
            unique.append((nums, stars))
        if len(unique) >= MAX_TICKETS:
            break

    # 4) Highlight & tally prizes
    total_prize = 0.0
    for idx, (nums, stars) in enumerate(unique, start=1):
        nums_i  = sorted(int(n) for n in nums)
        stars_i = sorted(int(s) for s in stars)

        hn = " ".join(f"*{n:02d}*" if n in draw_nums else f" {n:02d} " for n in nums_i)
        hs = " ".join(f"*{s:02d}*" if s in draw_strs else f" {s:02d} " for s in stars_i)

        matched_n = len(set(nums_i) & set(draw_nums))
        matched_s = len(set(stars_i) & set(draw_strs))
        prize_info = next(
            (p for p in draw_row.get("prizes", [])
             if p["matched_numbers"] == matched_n and p["matched_stars"] == matched_s),
            None
        )
        prize = prize_info["prize"] if prize_info else 0.0
        total_prize += prize

        print(f"Ticket {idx}: {hn} ({hs}) → €{prize:,.2f}")

    print(f"--- Total won this draw: €{total_prize:,.2f}")


def format_tickets(raw_tickets: List[Ticket]) -> List[Formatted]:
    formatted = []
    for nums, stars in raw_tickets:
        nums_i  = sorted(int(n) for n in nums)
        stars_i = sorted(int(s) for s in stars)
        formatted.append((
            [f"{n:02d}" for n in nums_i],
            [f"{s:02d}" for s in stars_i]
        ))
    return formatted


def dedupe_and_limit(
        raw: List[Ticket],
        limit: int = MAX_TICKETS
) -> List[Ticket]:
    seen = set()
    out = []
    for nums, stars in raw:
        key = (
            tuple(sorted(int(x) for x in nums)),
            tuple(sorted(int(x) for x in stars))
        )
        if key not in seen:
            seen.add(key)
            out.append((nums, stars))
        if len(out) >= limit:
            break
    return out


def print_aligned_tickets(tickets: List[Formatted], title: str):
    print(f"\n{title}")
    print(f"{'Ticket':<6} | {'Numbers':<17} | {'Stars'}")
    print(f"{'-'*6}-+-{'-'*17}-+-{'-'*5}")
    for idx, (nums, stars) in enumerate(tickets, start=1):
        print(f"{idx:<6} | {' '.join(nums):<17} | {' '.join(stars)}")


def run_evolution():
    draws_df  = load_draws_df()
    prizes_df = load_prizes_df()
    variants  = get_all_strategy_variants()
    num_strat = len(variants)

    # initial population & scores
    population = initialize_population(num_strat, POPULATION_SIZE)
    scores     = [0.0] * POPULATION_SIZE

    best_global_score = float("-inf")
    best_global_chrom = None

    draws_len = len(draws_df)
    for draw_idx, draw_row in draws_df.iterrows():
        idx_plus_1 = draw_idx + 1
        if SLIDING_WINDOW is not None and idx_plus_1 < SLIDING_WINDOW:
            continue

        window_start = 0 if SLIDING_WINDOW is None else max(0, draw_idx - SLIDING_WINDOW + 1)
        window_df    = draws_df.iloc[window_start: idx_plus_1]
        window_len   = len(window_df)

        print(f"\n=== Draw {idx_plus_1}/{draws_len} using last {window_len} draws ===")

        # score initial population
        scores = [
            score_chromosome(chrom, variants, window_df, prizes_df)
            for chrom in population
        ]

        # evolve on this window
        population, scores, best_local_chrom, best_local_score = evolve_window(
            population, scores, variants, window_df, prizes_df
        )

        # out‑of‑sample report on NEXT draw
        next_idx = draw_idx + 1
        if next_idx < draws_len:
            next_row = draws_df.iloc[next_idx]
            report_draw(next_idx, next_row, best_local_chrom, variants, window_df)

        # track all‑time best chromosome
        if best_local_score > best_global_score:
            best_global_score = best_local_score
            best_global_chrom = best_local_chrom

    # Final recommendation for next draw
    raw_final = generate_tickets_from_variants(
        best_global_chrom, variants, draws_df, MAX_TICKETS
    )
    raw_final = dedupe_and_limit(raw_final, MAX_TICKETS)
    formatted = format_tickets(raw_final)
    print_aligned_tickets(formatted, "=== Final Recommended Tickets for Next Draw ===")


if __name__ == "__main__":
    run_evolution()
