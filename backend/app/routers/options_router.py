from fastapi import APIRouter, Query, HTTPException
from app.schemas.options_schema import OptionChainResponse, PricingRequest, PricingResponse, OptionChainRequest, PricedOptionChainResponse, PricedContract
from services.options_service import get_polygon_option_contracts
from services import volatility_service
from datetime import datetime
import pricing_cpp # type: ignore

router = APIRouter(
    prefix="/options",
    tags=["Options"]
)

@router.get("/", response_model=OptionChainResponse)
async def fetch_option_contracts(ticker: str = Query(..., description="Stock Ticker Symbol"), 
                                 type: str = Query(None, description="Call or Put"),
                                 expiration: str = Query(None, description="Expiration Date"),
                                 min_strike: float = Query(None, description="Minimum Strike Price"),
                                 max_strike: float = Query(None, description="Maximum Strike Price")):
    try:
        contracts_raw = await get_polygon_option_contracts(
            ticker=ticker,
            option_type=type,
            expiration_date=expiration,
            min_strike_price=min_strike,
            max_strike_price=max_strike
        )
        
        contracts = [{
            "type": c.get("contract_type"),
            "strike": c.get("strike_price"),
            "expiration": c.get("expiration_date"),
            "symbol": c.get("ticker"),
        } for c in contracts_raw]

        return OptionChainResponse(ticker=ticker.upper(), contracts=contracts)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

@router.post("/price", response_model=PricingResponse)
async def price_option(request: PricingRequest):
    try:
        result = 0.0
        if request.model == 'binomial_tree':
            result = pricing_cpp.binomial_tree_calculator(request.S, request.K, request.T, request.r, request.sigma, request.steps, request.option_type, request.is_american)
        elif request.model == 'black_scholes':
            if request.is_american:
                raise ValueError("Black-Scholes model can only be used for European options.")
            result = pricing_cpp.black_scholes_calculator(request.S, request.K, request.T, request.r, request.sigma, request.option_type)
        return {"price": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chain/price", response_model=PricedOptionChainResponse)
async def price_full_option_chain(request: OptionChainRequest):
    try:
        volatility, underlying_price= await volatility_service.estimate_historical_volatility(request.ticker)
        risk_free_rate = 0.0425
        contracts = await get_polygon_option_contracts(
            ticker=request.ticker,
            option_type=request.option_type,
            expiration_date=request.expiration_date,
            min_strike_price=request.min_strike_price,
            max_strike_price=request.max_strike_price
        )

        priced_contracts = []
        today = datetime.now().date()

        for contract in contracts:
            expiration = datetime.strptime(contract['expiration_date'], '%Y-%m-%d').date()
            time_to_maturity = (expiration - today).days / 365.25

            if time_to_maturity > 0:
                price = pricing_cpp.binomial_tree_calculator(
                    S=underlying_price, K=contract['strike_price'], T=time_to_maturity,
                    r=risk_free_rate, sigma=volatility, steps=1000,
                    option_type=contract['contract_type'], is_american=True
                )
                priced_contracts.append(PricedContract(
                    symbol=contract['ticker'], strike_price=contract['strike_price'],
                    option_type=contract['contract_type'], expiration_date=contract['expiration_date'],
                    calculated_price=price
                ))
        
        return PricedOptionChainResponse(
            ticker=request.ticker.upper(), underlying_price=underlying_price,
            volatility=volatility, risk_free_rate=risk_free_rate,
            priced_contracts=priced_contracts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))