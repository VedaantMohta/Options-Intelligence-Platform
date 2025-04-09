import requests
from config import POLYGON_API_KEY

def get_polygon_option_contracts(ticker: str) -> dict:
    url = (
        f"https://api.polygon.io/v3/reference/options/contracts"
        f"?underlying_ticker={ticker.upper()}&expired=false&limit=50&apiKey={POLYGON_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Polygon API request failed with status {response.status_code}")
    
    data = response.json()
    contracts_raw = data.get("results", [])
    contracts = []

    for contract in contracts_raw:
        contracts.append({
            "type": contract.get("contract_type"),
            "strike": contract.get("strike_price"),
            "expiration": contract.get("expiration_date"),
            "symbol": contract.get("ticker"),
        })
    
    return {
        "ticker": ticker.upper(),
        "contracts": contracts
    }