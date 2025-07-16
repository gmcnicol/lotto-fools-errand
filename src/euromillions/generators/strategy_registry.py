from .ticket_generator import generate_tickets_from_variants
from .strategies.frequency_weighted import get_variants as frequency_weighted_variants
from .strategies.hot_cold import get_variants as hot_cold_variants
__all__ = ["get_all_strategy_variants", "generate_tickets_from_variants"]

def get_all_strategy_variants() -> list:
    variants = []
    variants.extend(frequency_weighted_variants())
    # add other strategy‐variant imports here:
    # from .strategies.hot_cold import get_variants as hot_cold_variants
    variants.extend(hot_cold_variants())
    return variants
