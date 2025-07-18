import logging
import math
from collections import Counter
import pandas as pd

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION FLAGS & WEIGHTS
# Toggle each term on/off here:
USE_PRIZE_SCORE      = True
USE_FREQ_PENALTY     = True
USE_UNIFORMITY_PENALTY = True
USE_ENTROPY_BONUS    = True
USE_PATTERN_PENALTY  = True

# If you disable a term, its weight is ignored.
FREQ_PENALTY_WEIGHT      = 0.1   # α
UNIFORMITY_PENALTY_WEIGHT = 0.1   # β
ENTROPY_BONUS_WEIGHT     = 0.05  # γ
PATTERN_PENALTY_WEIGHT   = 1.0   # δ
# ─────────────────────────────────────────────────────────────

def evaluate_ticket_set(
        tickets: list[tuple[list[int], list[int]]],
        draws_df: pd.DataFrame,
        prizes_df: pd.DataFrame = None
) -> tuple[float, float]:
    """
    1) Normalize tickets → ensure all nums & stars are ints
    2) Prize‐only score (if enabled)
    3) Frequency penalty
    4) Uniformity penalty
    5) Entropy bonus
    6) Pattern penalty (straight‐line / arithmetic sequences)
    """
    # 1) Normalize
    clean_tix = []
    for nums, stars in tickets:
        clean_nums  = [int(n) for n in nums]
        clean_stars = [int(s) for s in stars]
        clean_tix.append((clean_nums, clean_stars))
    tickets = clean_tix

    # 2) Prize‐only score
    prize_score = 0.0
    if USE_PRIZE_SCORE:
        for _, row in draws_df.iterrows():
            draw_nums  = set(map(int, row["numbers"]))
            draw_stars = set(map(int, row["stars"]))
            prize_list = row.get("prizes", [])
            for ticket_nums, ticket_stars in tickets:
                matched_n = len(draw_nums.intersection(ticket_nums))
                matched_s = len(draw_stars.intersection(ticket_stars))
                pi = next(
                    (p for p in prize_list
                     if p["matched_numbers"] == matched_n
                     and p["matched_stars"]   == matched_s),
                    None
                )
                if pi:
                    prize_score += pi.get("prize", 0.0)

    # Build flat count of picks
    num_counts = Counter()
    total_picks = 0
    for nums, _ in tickets:
        for n in nums:
            num_counts[n] += 1
            total_picks += 1
    counts = [num_counts.get(i, 0) for i in range(1, 51)]

    # 3) Frequency penalty
    freq_pen = sum(c**2 for c in counts) if USE_FREQ_PENALTY else 0.0

    # 4) Uniformity penalty
    uniformity_pen = 0.0
    if USE_UNIFORMITY_PENALTY:
        ideal = total_picks / 50
        uniformity_pen = sum((c - ideal)**2 for c in counts)

    # 5) Entropy bonus
    entropy_bonus = 0.0
    if USE_ENTROPY_BONUS and total_picks > 0:
        ent = 0.0
        for c in counts:
            if c > 0:
                p = c / total_picks
                ent -= p * math.log(p)
        entropy_bonus = ent

    # 6) Pattern penalty
    pattern_pen = _pattern_penalty(tickets) if USE_PATTERN_PENALTY else 0.0

    # Combine
    fitness = 0.0
    if USE_PRIZE_SCORE:
        fitness += prize_score
    if USE_FREQ_PENALTY:
        fitness -= FREQ_PENALTY_WEIGHT * freq_pen
    if USE_UNIFORMITY_PENALTY:
        fitness -= UNIFORMITY_PENALTY_WEIGHT * uniformity_pen
    if USE_ENTROPY_BONUS:
        fitness += ENTROPY_BONUS_WEIGHT * entropy_bonus
    if USE_PATTERN_PENALTY:
        fitness -= PATTERN_PENALTY_WEIGHT * pattern_pen

    logger.debug(
        f"Breakdown → prize: {prize_score:.2f}, freq_pen: {freq_pen:.2f}, "
        f"uni_pen: {uniformity_pen:.2f}, entropy: {entropy_bonus:.4f}, "
        f"pattern_pen: {pattern_pen:.1f} → total {fitness:.2f}"
    )
    return fitness, prize_score


def _pattern_penalty(tickets: list[tuple[list[int], list[int]]]) -> float:
    """
    +1 penalty for any ticket whose numbers form an exact arithmetic
    sequence (i.e. all diffs equal).
    """
    penalty = 0.0
    for nums, _ in tickets:
        if len(nums) < 2:
            continue
        # ensure ints (should already be)
        nums = [int(n) for n in nums]
        diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
        if len(set(diffs)) == 1:
            penalty += 1.0
    return penalty
