from services.options_service import get_polygon_option_contracts

result = get_polygon_option_contracts(
    ticker="AAPL",
    type="call",
    min_strike=105,
    max_strike=117
)

print(f"Filtered contracts: {len(result['contracts'])}")
for contract in result["contracts"]:
    print(contract)
