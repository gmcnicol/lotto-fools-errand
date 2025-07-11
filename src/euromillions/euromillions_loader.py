import os
import requests
import pandas as pd

DATA_DIR = "data"
CACHE_PATH = os.path.join(DATA_DIR, "euromillions_draws.parquet")
API_URL = "https://euromillions.api.pedromealha.dev/v1/draws"

def fetch_draws():
    print("Fetching EuroMillions draw history from API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def parse_draws(raw_draws):
    records = [
        {
            "draw_date": draw["date"],
            "numbers": draw["numbers"],
            "stars": draw["stars"]
        }
        for draw in raw_draws
    ]
    df = pd.DataFrame(records)
    df["draw_date"] = pd.to_datetime(df["draw_date"])
    return df.sort_values("draw_date")

def load_draws(force_refresh=False):
    os.makedirs(DATA_DIR, exist_ok=True)

    if not force_refresh and os.path.exists(CACHE_PATH):
        print(f"Loading draws from cache: {CACHE_PATH}")
        return pd.read_parquet(CACHE_PATH)

    raw = fetch_draws()
    df = parse_draws(raw)
    df.to_parquet(CACHE_PATH, index=False)
    print(f"Cached draws to: {CACHE_PATH}")
    return df

if __name__ == "__main__":
    df = load_draws()
    print(df.head())
