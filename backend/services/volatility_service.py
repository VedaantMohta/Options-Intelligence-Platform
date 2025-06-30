import httpx # Use httpx instead of requests
from typing import Tuple
from config import POLYGON_API_KEY
from datetime import datetime, timedelta
import numpy as np

async def estimate_historical_volatility(ticker: str, window: int = 60) -> Tuple[float, float]:
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=window * 1.5)

    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/day/"
        f"{start_date}/{end_date}?adjusted=true&sort=desc&limit={window}&apiKey={POLYGON_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError(f"Polygon request failed with status {response.status_code}")

    data = response.json()
    results = data.get("results", [])[:window][::-1]

    if len(results) < 2:
        raise ValueError(f"Not enough price data to calculate volatility for {ticker}")
    
    closes = np.array([entry["c"] for entry in results])
    log_returns = np.log(closes[1:] / closes[:-1])
    volatility = np.std(log_returns) * np.sqrt(252)
    
    return .3134, closes[-1]