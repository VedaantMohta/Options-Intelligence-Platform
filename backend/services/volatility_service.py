import requests
from typing import Optional
from config import POLYGON_API_KEY
from datetime import datetime, timedelta
import numpy as np

def estimate_historical_volatility(ticker: str, window: int = 35):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=window * 1.5)

    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/day/"
        f"{start_date}/{end_date}?adjusted=true&sort=desc&limit={window}&apiKey={POLYGON_API_KEY}"
    )

    response = requests.get(url)

    # Handle errors early
    if response.status_code != 200:
        raise ValueError(f"Polygon request failed with status {response.status_code}")

    data = response.json()

    # Get the list of price points
    results = data.get("results", [])[:window][::-1]
    if len(results) < 2:
        raise ValueError(f"Not enough price data to calculate volatility for {ticker}")
    
    # Calculating standard deviation
    closes = [entry["c"] for entry in results]
    closes = np.array(closes)
    returns = np.log(closes[1:] / closes [:-1])
    volatility = np.std(returns) * np.sqrt(252)
    print(volatility)
    return volatility, closes[-1]
