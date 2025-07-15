import logging
import math
from collections import Counter
import pandas as pd

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION FLAGS & WEIGHTS
# Toggle each term on/off here:
USE_PRIZE_SCORE = True
USE_FREQ_PENALTY = True
USE_UNIFORMITY_PENALTY = True
USE_ENTROPY_BONUS = True

# If you disable a term, its weight is ignored.
FREQ_PENALTY_WEIGHT = 0.1       # α
UNIFORMITY_PENALTY_WEIGHT = 0.1 # β
ENTROPY_BONUS_WEIGHT = 0.05     # γ
# ─────────────────────────────────────────────────────────────

def evaluate_ticket_set(
        tickets: list[tuple[list[int], list[int]]],
        draws_df: pd.DataFrame,
        prizes_df: pd.DataFrame = None  # not used if USE_PRIZE_SCORE is False
) -> float:
    """
    Combines:
      1) historical payout over draws_df (prize-only)
      2) frequency penalty (repeats within the ticket-set)
      3) uniformity penalty (deviation from ideal spread)
      4) entropy bonus (Shannon entropy of picks)
    according to the flags/weights above.
    """
    # 1) Prize‐only score: sum of all prizes won across historical draws
    prize_score = 0.0
    if USE_PRIZE_SCORE:
        for _, row in draws_df.iterrows():
            draw_numbers = set(map(int, row["numbers"]))
            draw_stars   = set(map(int, row["stars"]))
            prize_list   = row.get("prizes", [])

            for ticket_nums, ticket_stars in tickets:
                matched_n = len(draw_numbers.intersection(ticket_nums))
                matched_s = len(draw_stars.intersection(ticket_stars))
                # find matching prize tier
                prize_info = next(
                    (p for p in prize_list
                     if p.get("matched_numbers") == matched_n
                     and   p.get("matched_stars")   == matched_s),
                    None
                )
                if prize_info:
                    prize_score += prize_info.get("prize", 0.0)

    # Build a flat count of how often each number (1–50) appears in our ticket set:
    number_counts = Counter()
    total_picks = 0
    for ticket_nums, _ in tickets:
        for n in ticket_nums:
            number_counts[n] += 1
            total_picks += 1

    # Prepare the full 1–50 list (zeros if never picked)
    counts = [number_counts.get(i, 0) for i in range(1, 51)]

    # 2) Frequency penalty: sum of squares of counts
    freq_penalty = 0.0
    if USE_FREQ_PENALTY:
        freq_penalty = sum(c**2 for c in counts)

    # 3) Uniformity penalty: sum of squared deviations from ideal
    uniformity_penalty = 0.0
    if USE_UNIFORMITY_PENALTY:
        ideal = total_picks / 50
        uniformity_penalty = sum((c - ideal)**2 for c in counts)

    # 4) Entropy bonus: Shannon entropy of the distribution
    entropy_bonus = 0.0
    if USE_ENTROPY_BONUS and total_picks > 0:
        entropy = 0.0
        for c in counts:
            if c > 0:
                p = c / total_picks
                entropy -= p * math.log(p)
        entropy_bonus = entropy

    # Combine everything
    fitness = 0.0
    if USE_PRIZE_SCORE:
        fitness += prize_score
    if USE_FREQ_PENALTY:
        fitness -= FREQ_PENALTY_WEIGHT * freq_penalty
    if USE_UNIFORMITY_PENALTY:
        fitness -= UNIFORMITY_PENALTY_WEIGHT * uniformity_penalty
    if USE_ENTROPY_BONUS:
        fitness += ENTROPY_BONUS_WEIGHT * entropy_bonus

    # Log (at debug level) the breakdown
    logger.debug(
        f"Score breakdown → prize: {prize_score:.2f}, "
        f"freq_penalty: {freq_penalty:.2f}, "
        f"uniformity_penalty: {uniformity_penalty:.2f}, "
        f"entropy_bonus: {entropy_bonus:.4f}, "
        f"→ total fitness: {fitness:.2f}"
    )

    return fitness
