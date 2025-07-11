from typing import List, Tuple

Ticket = Tuple[List[int], List[int]]

def round_robin_dedup(ticket_sets: List[List[Ticket]], max_len: int) -> List[Ticket]:
    seen = set()
    result = []

    while ticket_sets and len(result) < max_len:
        new_ticket_sets = []
        for ticket_set in ticket_sets:
            if ticket_set:
                ticket = ticket_set.pop(0)
                if ticket not in seen:
                    result.append(ticket)
                    seen.add(ticket)
                if ticket_set:
                    new_ticket_sets.append(ticket_set)
        ticket_sets = new_ticket_sets

    return result
