import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DRAWS_PATH = DATA_DIR / "draws.parquet"

DRAW_API_URL = "https://euromillions.api.pedromealha.dev/v1/draws"

def fetch_and_cache_draws():
    response = requests.get(DRAW_API_URL)
    response.raise_for_status()
    draw_list = response.json()

    rows = []
    for draw in draw_list:
        draw_id = int(draw["id"])
        date = draw["date"]
        main = draw.get("numbers", [])
        stars = draw.get("stars", [])
        prizes = draw.get("prizes", [])

        rows.append({
            "draw_id": draw_id,
            "date": datetime.strptime(date, "%Y-%m-%d"),
            "main_numbers": [int(n) for n in main],
            "lucky_stars": [int(s) for s in stars],
            "prizes": prizes,
            "has_winner": any(p.get("winners", 0) > 0 for p in prizes),
        })

    df = pd.DataFrame(rows)
    df.to_parquet(DRAWS_PATH, index=False)

def load_draws() -> pd.DataFrame:
    return pd.read_parquet(DRAWS_PATH)

def load_prizes(draw_id: int) -> list[dict]:
    df = load_draws()
    row = df[df["draw_id"] == draw_id]
    if not row.empty:
        return row.iloc[0]["prizes"]
    return []
