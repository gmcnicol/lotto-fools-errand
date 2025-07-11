from euromillions.genetics.genome import generate_random_chromosome, mutate_chromosome, evaluate_chromosome
from euromillions.generators.strategy_registry import get_all_strategy_variants

MAX_ITERATIONS = 10000
STABILITY_THRESHOLD = 5

def run_evolution():
    population = []
    scores = []
    history = []

    strategy_count = len(get_all_strategy_variants())

    for i in range(MAX_ITERATIONS):
        if i == 0:
            chromosome = generate_random_chromosome(strategy_count)
        else:
            chromosome = mutate_chromosome(population[-1])

        score = evaluate_chromosome(chromosome)
        population.append(chromosome)
        scores.append(score)
        history.append((chromosome, score))

        print(f"Generation {i + 1}: Chromosome={chromosome}, Score={score}")

        if len(history) >= STABILITY_THRESHOLD and all(s == history[-1][1] for _, s in history[-STABILITY_THRESHOLD:]):
            print(f"Converged after {i+1} generations")
            break

    best_chromosome, best_score = max(history, key=lambda x: x[1])
    print("\nBest Chromosome:", best_chromosome)
    print("Best Score:", best_score)

    from euromillions.euromillions_loader import load_draws_df
    from euromillions.generators.ticket_generator import generate_tickets_from_variants

    from euromillions.generators.strategy_registry import get_all_strategy_variants
    all_variants = get_all_strategy_variants()
    selected_variants = [
        variant for gene, variant in zip(best_chromosome, all_variants) if gene
    ]
    draws_df = load_draws_df()
    tickets = generate_tickets_from_variants(draws_df, selected_variants, max_tickets=7)

    print("\nSuggested Tickets to Play:")
    for i, t in enumerate(tickets[:7], 1):
        print(f"Ticket {i}: {t}")
