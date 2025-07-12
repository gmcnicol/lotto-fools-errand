import logging

import pandas as pd
import requests

DRAW_URL = "https://euromillions.api.pedromealha.dev/v1/draws"
DRAW_PATH = "data/draws.parquet"
PRIZE_PATH = "data/prizes.parquet"

def fetch_and_cache_draws():
    response = requests.get(DRAW_URL)
    draws = response.json()
    draws_df = pd.DataFrame(draws)
    draws_df.to_parquet(DRAW_PATH)
    draws_df.to_parquet(PRIZE_PATH)

def load_draws_df():
    return pd.read_parquet(DRAW_PATH)

def load_prizes_df():
    logger = logging.getLogger(__name__)
    logger.info("Loading prizes DataFrame from cache or file.")
    ret = pd.read_parquet(PRIZE_PATH)
    logger.info(ret.head())

    return ret
