from fastapi import APIRouter, Query, HTTPException
from app.schemas.options_schema import OptionChainResponse, PricingRequest
from services.options_service import get_polygon_option_contracts
import pricing_cpp # type: ignore

router = APIRouter()

@router.get("/")
def fetch_option_contracts(ticker: str = Query(..., description="Stock Ticker Symbol"), 
                           type: str = Query(None, description="Call or Put"),
                           expiration: str = Query(None, description="Expiration Date"),
                           min_strike: float = Query(None, description="Minimum Strike Price"),
                           max_strike: float = Query(None, description="Maximum Strike Price")):
    try:
        return get_polygon_option_contracts(ticker,
                                            type=type,
                                            expiration=expiration,
                                            min_strike=min_strike,
                                            max_strike=max_strike)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

@router.post("/price")
def price_option(request: PricingRequest):
    try:
        result = pricing_cpp.calculate_option_price(
            request.S,
            request.K,
            request.T,
            request.r,
            request.sigma,
            request.option_type
        )
        return {"price": result}
    except Exception as e:
        return {"error": str(e)}