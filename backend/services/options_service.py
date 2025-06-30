import httpx
from typing import Optional, List, Dict
from config import POLYGON_API_KEY

async def get_polygon_option_contracts(ticker: str,
                                       option_type: Optional[str] = None,
                                       expiration_date: Optional[str] = None,
                                       min_strike_price: Optional[float] = None,
                                       max_strike_price: Optional[float] = None) -> List[Dict]:
    
    base_url = "https://api.polygon.io/v3/reference/options/contracts"
    
    params = {
        'apiKey': POLYGON_API_KEY,
        'underlying_ticker': ticker.upper(),
        'expired': 'false',
        'limit': 1000
    }

    if option_type:
        params['contract_type'] = option_type.lower()
    if expiration_date:
        params['expiration_date'] = expiration_date
    if min_strike_price is not None:
        params['strike_price.gte'] = min_strike_price
    if max_strike_price is not None:
        params['strike_price.lte'] = max_strike_price

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
    
    if response.status_code != 200:
        raise ValueError(f"Polygon API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("results", [])