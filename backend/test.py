from services.volatility_service import estimate_historical_volatility

if __name__ == "__main__":
    ticker = "COST"
    try:
        vol = estimate_historical_volatility(ticker)
        print(f"Estimated volatility for {ticker}: {vol:.4f}")
    except Exception as e:
        print(f"Error: {e}")
