from .strategies.frequency_weighted import get_variants as frequency_weighted_variants
from .strategies.hot_cold import get_variants as hot_cold_variants
from .strategies.markov_chain import get_variants as markov_chain_variants
from .strategies.age_weighted import get_variants as age_weighted_variants
from .strategies.decay_weighted import get_variants as decay_weighted_variants
from .strategies.pair_frequency import get_variants as pair_frequency_variants
from .strategies.parity_balance import get_variants as parity_balance_variants
from .strategies.sum_target import get_variants as sum_target_variants
from .ticket_generator import generate_tickets_from_variants

__all__ = ["get_all_strategy_variants", "generate_tickets_from_variants"]


def get_all_strategy_variants() -> list:
    variants = []
    variants.extend(frequency_weighted_variants())
    variants.extend(hot_cold_variants())
    variants.extend(markov_chain_variants())
    variants.extend(age_weighted_variants())
    variants.extend(decay_weighted_variants())
    variants.extend(pair_frequency_variants())
    variants.extend(parity_balance_variants())
    variants.extend(sum_target_variants())
    return variants
