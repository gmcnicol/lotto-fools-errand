import pandas as pd
import os
import requests

DRAW_URL = "https://euromillions.api.pedromealha.dev/v1/draws"
DRAW_PATH = "data/draws.parquet"
PRIZE_PATH = "data/prizes.parquet"

def fetch_and_cache_draws():
    response = requests.get(DRAW_URL)
    draws = response.json()
    draws_df = pd.DataFrame(draws)
    draws_df.to_parquet(DRAW_PATH)
    draws_df.to_parquet(PRIZE_PATH)  # assuming same for placeholder

def load_draws_df():
    return pd.read_parquet(DRAW_PATH)

def load_prizes_df():
    return pd.read_parquet(PRIZE_PATH)
