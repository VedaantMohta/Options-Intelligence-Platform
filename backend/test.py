from services.options_service import price_option_from_source

test_contract = {
    "type": "call",
    "strike": 113,
    "expiration": "2025-06-20",  # must match YYYY-MM-DD format
    "symbol": "O:AAPL250419C00205000"
}

price = price_option_from_source("NVDA", test_contract)
print(f"Calculated Option Price: {price:.4f}")
