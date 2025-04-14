import requests
import pricing_cpp # type: ignore
from typing import Optional
from config import POLYGON_API_KEY
from datetime import datetime, timedelta
from services.volatility_service import estimate_historical_volatility

def get_polygon_option_contracts(ticker: str,
                                 type: Optional[str] = None,
                                 expiration: Optional[str] = None,
                                 min_strike: Optional[float] = None,
                                 max_strike: Optional[float] = None) -> dict:
    url = (
        f"https://api.polygon.io/v3/reference/options/contracts"
        f"?underlying_ticker={ticker.upper()}&expired=false&limit=1000&apiKey={POLYGON_API_KEY}"
    )

    if type:
        url += f"&contract_type={type.lower()}"
    if expiration:
        url += f"&expiration_date={expiration}"
    if min_strike is not None:
        url += f"&strike_price.gte={min_strike}"
    if max_strike is not None:
        url += f"&strike_price.lte={max_strike}"


    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Polygon API request failed with status {response.status_code}")
    
    data = response.json()
    contracts_raw = data.get("results", [])
    contracts = []

    for contract in contracts_raw:
        if type and contract.get("contract_type", "").lower() != type.lower(): continue
        if expiration and contract.get("expiration_date") != expiration: continue
        strike = contract.get("strike_price")
        if min_strike is not None and strike < min_strike: continue
        if max_strike is not None and strike > max_strike: continue
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

def price_option_from_source(ticker: str, contract: dict) -> float:
    sigma, S = estimate_historical_volatility(ticker)
    K = contract["strike"]
    expiration_date = datetime.strptime(contract["expiration"], "%Y-%m-%d").date()
    days_to_exp = (expiration_date - datetime.today().date()).days
    T = days_to_exp / 252
    r = 0.0426
    option_type = contract["type"].lower()

    return pricing_cpp.calculate_option_price(S, K, T, r, sigma, option_type)