def generate_tickets_from_variants(
        chromosome: list[int],
        variants: list[callable],
        draws_df,        # pandas.DataFrame of past draws (or sliding window)
        max_tickets: int
) -> list[tuple[list[int], list[int]]]:
    """
    Given a binary chromosome and a list of strategy fns (variants),
    run each active strategy to produce up to max_tickets total.
    """
    active = [fn for bit, fn in zip(chromosome, variants) if bit]
    tickets: list[tuple[list[int], list[int]]] = []
    if not active:
        return tickets

    per = max_tickets // len(active)
    extra = max_tickets % len(active)

    for idx, gen_fn in enumerate(active):
        cnt = per + (1 if idx < extra else 0)
        if cnt > 0:
            tickets.extend(gen_fn(draws_df, cnt))

    return tickets
