from euromillions.genetics.genome import (
    Chromosome,
    generate_random_chromosome,
    evaluate_chromosome,
)
from euromillions.generators.ticket_generator import generate_tickets_from_variants
from euromillions.generators.strategy_registry import get_all_strategy_variants
from euromillions.euromillions_loader import load_draws_df

def run_all_genomes(max_iterations=10000, convergence_threshold=5):
    draws_df = load_draws_df()
    all_variants = get_all_strategy_variants()
    strategy_count = len(all_variants)

    best_score = 0.0
    best_chromosome = []
    best_tickets = []

    recent_top_scores = []

    for i in range(max_iterations):
        chromo: Chromosome = generate_random_chromosome(strategy_count)
        score = evaluate_chromosome(chromo)

        if score > best_score:
            selected_variants = [
                variant for gene, variant in zip(chromo, all_variants) if gene
            ]
            best_tickets = generate_tickets_from_variants(draws_df, selected_variants)
            best_score = score
            best_chromosome = chromo

        recent_top_scores.append(best_score)
        if len(recent_top_scores) > convergence_threshold:
            recent_top_scores.pop(0)
            if all(s == recent_top_scores[0] for s in recent_top_scores):
                break

    print("\nFittest Chromosome:", best_chromosome)
    print("Score:", best_score)
    print("Tickets to play:")
    for ticket in best_tickets:
        numbers, stars = ticket
        print(f"  Numbers: {sorted(numbers)}  Stars: {sorted(stars)}")
