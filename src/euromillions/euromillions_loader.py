# src/euromillions/euromillions_loader.py

import os
import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
DRAWS_FILE = os.path.join(DATA_DIR, "draws.parquet")
PRIZES_FILE = os.path.join(DATA_DIR, "prizes.parquet")
API_URL = "https://euromillions.api.pedromealha.dev/v1/draws"


def fetch_and_cache_draws():
    print(f"Fetching draws from: {API_URL}")
    response = requests.get(API_URL)
    response.raise_for_status()
    draws = response.json()

    rows = []
    prize_rows = []

    for draw in draws:
        draw_id = draw["id"]
        date = draw["date"]
        main_numbers = draw["numbers"]["main"]
        lucky_stars = draw["numbers"]["luckyStars"]
        has_winner = draw["hasWinner"]

        rows.append({
            "draw_id": draw_id,
            "date": date,
            "main_numbers": main_numbers,
            "lucky_stars": lucky_stars,
            "has_winner": has_winner,
        })

        prize_breakdown = draw.get("prizeBreakdown", {})
        flat = {"draw_id": draw_id}
        for tier, prize in prize_breakdown.items():
            key = f"{prize['matchedNumbers']}+{prize['matchedStars']}"
            flat[key] = prize.get("prize", 0.0)
        prize_rows.append(flat)

    os.makedirs(DATA_DIR, exist_ok=True)
    pd.DataFrame(rows).to_parquet(DRAWS_FILE, index=False)
    pd.DataFrame(prize_rows).to_parquet(PRIZES_FILE, index=False)


def load_draws_df():
    return pd.read_parquet(DRAWS_FILE)


def load_prizes_df():
    return pd.read_parquet(PRIZES_FILE)
