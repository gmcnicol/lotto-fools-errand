from typing import List, Tuple, Dict


def evaluate_ticket(
        ticket_main: List[int],
        ticket_stars: List[int],
        draw_main: List[int],
        draw_stars: List[int],
) -> Dict[str, int]:
    """
    Compare a single ticket to a winning draw and return match counts.

    Returns a dictionary like:
    {
        "main_matches": 3,
        "star_matches": 2
    }
    """
    main_matches = len(set(ticket_main) & set(draw_main))
    star_matches = len(set(ticket_stars) & set(draw_stars))

    return {
        "main_matches": main_matches,
        "star_matches": star_matches
    }


def evaluate_all_tickets(
        tickets: List[Tuple[List[int], List[int]]],
        draw_main: List[int],
        draw_stars: List[int]
) -> List[Dict[str, int]]:
    """
    Evaluate a batch of tickets against a winning draw.
    Returns list of match dicts, one per ticket.
    """
    return [
        evaluate_ticket(main, stars, draw_main, draw_stars)
        for main, stars in tickets
    ]
