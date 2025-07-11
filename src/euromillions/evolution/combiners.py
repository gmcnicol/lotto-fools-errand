from typing import List, Tuple

Ticket = Tuple[List[int], List[int]]

def round_robin_dedup(ticket_batches: List[Ticket], limit: int = 10) -> List[Ticket]:
    """
    Deduplicate and select up to `limit` tickets using round-robin.
    """
    seen = set()
    final = []

    for ticket in ticket_batches:
        key = (tuple(sorted(ticket[0])), tuple(sorted(ticket[1])))
        if key not in seen:
            seen.add(key)
            final.append(ticket)
        if len(final) == limit:
            break

    return final
