from typing import List, Dict, Tuple
import pandas as pd

from euromillions.generators.ticket_generator import generate_tickets
from euromillions.fitness.fitness import evaluate_ticket_set

# Declare strategies available in the system
ALL_STRATEGIES: Dict[str, str] = {
    "strategy_example": "strategy_example",
    # Add future strategies here: "strategy_name": "strategy_name"
}

Ticket = Tuple[List[int], List[int]]
Genome = List[int]

def test_genome(
        genome: Genome,
        draws_df: pd.DataFrame,
        step: int = 3,
        window: int = 100,
        tickets_per_strategy: int = 10
) -> float:
    """
    Given a binary genome and draw history, select enabled strategies,
    generate tickets, evaluate them against the most recent draw, and return fitness score.
    """

    if len(genome) != len(ALL_STRATEGIES):
        raise ValueError("Genome length must match number of strategies")

    selected_strategies = [
        name for enabled, name in zip(genome, ALL_STRATEGIES.keys()) if enabled
    ]

    print(f"🧬 Selected strategies: {selected_strategies}")

    all_tickets: List[Ticket] = []

    for strategy_name in selected_strategies:
        try:
            strategy_tickets = generate_tickets(
                strategy=strategy_name,
                draws_df=draws_df,
                step=step,
                window=window
            )
            all_tickets.extend(strategy_tickets[:tickets_per_strategy])
        except Exception as e:
            print(f"❌ Strategy {strategy_name} failed: {e}")

    # Deduplicate tickets (convert to hashable tuple-of-tuples)
    unique_tickets = list({tuple(tuple(x) for x in ticket) for ticket in all_tickets})
    print(f"🎟️  Generated {len(unique_tickets)} unique tickets.")

    # Score against most recent draw
    last_draw = draws_df.iloc[-1]
    fitness_score = evaluate_ticket_set(unique_tickets, last_draw)

    print(f"💰 Fitness score: £{fitness_score:,.2f}")
    return fitness_score
