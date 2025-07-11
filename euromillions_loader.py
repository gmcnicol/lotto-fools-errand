import requests
import pandas as pd
import os

API_URL = "https://euromillions.api.pedromealha.dev/v1/draws"
CACHE_PATH = "euromillions_draws.parquet"

def fetch_draws():
    print("Fetching EuroMillions draw history from API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    print(f"Fetched {len(data)} draws.")
    return data

def parse_draws(raw_draws):
    records = []
    for draw in raw_draws:
        record = {
            "draw_date": draw["date"],
            "numbers": draw["numbers"],
            "stars": draw["stars"]
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    df["draw_date"] = pd.to_datetime(df["draw_date"])
    return df.sort_values("draw_date")

def load_draws(force_refresh=False):
    if not force_refresh and os.path.exists(CACHE_PATH):
        print(f"Loading draws from local cache: {CACHE_PATH}")
        return pd.read_parquet(CACHE_PATH)
    
    raw = fetch_draws()
    df = parse_draws(raw)
    df.to_parquet(CACHE_PATH, index=False)
    print(f"Cached draws to: {CACHE_PATH}")
    return df

if __name__ == "__main__":
    df = load_draws()
    print(df.head())
